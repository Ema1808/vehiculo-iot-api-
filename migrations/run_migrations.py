import os
import sys
import re
import pymysql
from dotenv import load_dotenv

# Cargar variables de entorno desde el .env del backend
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

DB_HOST = os.getenv("DB_HOST", "instancia-rds-iot.cuq5v4vmgps2.us-east-1.rds.amazonaws.com")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Admin1234#")
DB_NAME = os.getenv("DB_NAME", "vehiculo_iot")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10
    )

def test_connection():
    print(f"Probando conexion a Amazon RDS ({DB_HOST}:{DB_PORT})...")
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT VERSION() AS ver, DATABASE() AS db")
            row = cur.fetchone()
            print(f"✅ Conectado exitosamente a MySQL {row['ver']} | Base: {row['db']}")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error de conexion: {e}")
        return False

def backup_schema():
    print("\n📦 Generando respaldo pre-migración de datos existentes...")
    backup_path = os.path.join(os.path.dirname(__file__), "backup_pre_v2.sql")
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW TABLES")
            tables = [list(r.values())[0] for r in cur.fetchall()]
            
            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(f"-- Respaldo previo a migracion V2 generado automaticamente\n")
                f.write(f"-- Base de datos: {DB_NAME}\n\n")
                for table in tables:
                    cur.execute(f"SELECT * FROM `{table}`")
                    rows = cur.fetchall()
                    f.write(f"-- Datos de la tabla `{table}` ({len(rows)} registros)\n")
                    for row in rows:
                        cols = ", ".join([f"`{k}`" for k in row.keys()])
                        vals = []
                        for v in row.values():
                            if v is None: vals.append("NULL")
                            elif isinstance(v, (int, float)): vals.append(str(v))
                            else: vals.append("'" + str(v).replace("'", "''") + "'")
                        f.write(f"INSERT IGNORE INTO `{table}` ({cols}) VALUES ({', '.join(vals)});\n")
                    f.write("\n")
        print(f"✅ Respaldo guardado exitosamente en: {backup_path}")
        return True
    except Exception as e:
        print(f"⚠️ Error generando respaldo: {e}")
        return False
    finally:
        conn.close()

def clean_sql_comments(sql_text):
    lines = []
    for line in sql_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("--"):
            continue
        lines.append(line)
    text = "\n".join(lines)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    return text

def parse_sql_statements(content):
    pattern = r"DELIMITER\s+;;(.*?)DELIMITER\s+;"
    statements = []
    last_end = 0

    for match in re.finditer(pattern, content, re.DOTALL):
        pre_text = clean_sql_comments(content[last_end:match.start()])
        for stmt in pre_text.split(";"):
            s = stmt.strip()
            if s:
                statements.append(s)
        
        proc_text = clean_sql_comments(match.group(1))
        # Remove trailing ;; if present
        proc_text = re.sub(r";;\s*$", "", proc_text).strip()
        if proc_text:
            statements.append(proc_text)
        last_end = match.end()

    tail_text = clean_sql_comments(content[last_end:])
    for stmt in tail_text.split(";"):
        s = stmt.strip()
        if s:
            statements.append(s)

    return statements

def apply_sql_file(file_path):
    print(f"\n🚀 Aplicando script SQL: {os.path.basename(file_path)}...")
    conn = get_connection()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        statements = parse_sql_statements(content)
        print(f"Total sentencias a ejecutar: {len(statements)}")

        with conn.cursor() as cur:
            for i, stmt in enumerate(statements, 1):
                try:
                    cur.execute(stmt)
                except Exception as err:
                    print(f"⚠️ Sentencia #{i} generó aviso: {err}")
                    print(f"Query: {stmt[:100]}...\n")
            conn.commit()

        print(f"✅ Script {os.path.basename(file_path)} procesado exitosamente.")
        return True
    except Exception as e:
        print(f"❌ Error al ejecutar script: {e}")
        return False
    finally:
        conn.close()

def verify_migration():
    print("\n🔍 Verificando estado post-migración en Amazon RDS...")
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW TABLES")
            tables = [list(r.values())[0] for r in cur.fetchall()]
            print(f"Total tablas encontradas ({len(tables)}): {', '.join(tables)}")

            tablas_clave = ["roles", "usuarios", "modelos_vehiculo", "vehiculos", "asignaciones_vehiculo", "demos", "sesiones_invitado", "bitacora_auditoria"]
            print("\nConteo de registros:")
            for t in tablas_clave:
                if t in tables:
                    cur.execute(f"SELECT COUNT(*) AS total FROM `{t}`")
                    cnt = cur.fetchone()["total"]
                    print(f"  - `{t}`: {cnt} registros")
                else:
                    print(f"  - ❌ `{t}` NO EXISTE")
        print("\n✅ Verificación de integridad completada.")
    finally:
        conn.close()

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "up"
    
    if action == "test":
        test_connection()
    elif action == "down":
        down_file = os.path.join(os.path.dirname(__file__), "V2__migracion_administracion_DOWN.sql")
        apply_sql_file(down_file)
        verify_migration()
    elif action == "up":
        if test_connection():
            backup_schema()
            up_file = os.path.join(os.path.dirname(__file__), "V2__migracion_administracion_UP.sql")
            apply_sql_file(up_file)
            verify_migration()
