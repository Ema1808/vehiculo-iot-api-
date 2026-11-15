import json
import secrets
from datetime import datetime, timedelta, timezone
from app.core.database import db_manager

class AdminRepository:
    """Encapsula las consultas y transacciones administrativas y de RBAC."""

    # --- USUARIOS Y AUTENTICACIÓN ---
    def obtener_usuario_por_email(self, email: str) -> dict:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT u.id_usuario, u.id_role, r.nombre AS rol, u.nombre_completo, 
                           u.email, u.password_hash, u.activo
                      FROM usuarios u
                      JOIN roles r ON u.id_role = r.id_role
                     WHERE u.email = %s
                """, (email,))
                return cur.fetchone()

    def crear_usuario(self, id_role: int, nombre: str, email: str, password_hash: str) -> int:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO usuarios (id_role, nombre_completo, email, password_hash, activo)
                    VALUES (%s, %s, %s, %s, 1)
                """, (id_role, nombre, email, password_hash))
                user_id = cur.lastrowid
                conn.commit()
                return user_id

    def obtener_usuarios(self, id_role: int = None) -> list:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                if id_role:
                    cur.execute("""
                        SELECT u.id_usuario, u.id_role, r.nombre AS rol, u.nombre_completo, 
                               u.email, u.activo, u.fecha_registro
                          FROM usuarios u
                          JOIN roles r ON u.id_role = r.id_role
                         WHERE u.id_role = %s
                         ORDER BY u.id_usuario ASC
                    """, (id_role,))
                else:
                    cur.execute("""
                        SELECT u.id_usuario, u.id_role, r.nombre AS rol, u.nombre_completo, 
                               u.email, u.activo, u.fecha_registro
                          FROM usuarios u
                          JOIN roles r ON u.id_role = r.id_role
                         ORDER BY u.id_usuario ASC
                    """)
                return cur.fetchall()

    # --- MODELOS COMERCIALES ---
    def obtener_modelos(self) -> list:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM modelos_vehiculo WHERE activo = 1 ORDER BY id_modelo ASC")
                return cur.fetchall()

    def crear_modelo(self, nombre: str, categoria: str, descripcion: str, microcontrolador: str) -> int:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO modelos_vehiculo (nombre, categoria, descripcion, microcontrolador_base, activo)
                    VALUES (%s, %s, %s, %s, 1)
                """, (nombre, categoria, descripcion, microcontrolador))
                mid = cur.lastrowid
                conn.commit()
                return mid

    # --- UNIDADES FÍSICAS (VEHÍCULOS AMPLIADOS) ---
    def obtener_unidades_ampliadas(self, user: dict = None) -> list:
        """
        Retorna las unidades con datos de modelo y asignación.
        Si user es USUARIO, filtra exclusivamente sus unidades asignadas.
        """
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT v.id_vehiculo, v.id_modelo, v.numero_serie, v.estado_comercial,
                           v.nombre, v.modelo, v.descripcion, v.microcontrolador, v.activo,
                           m.nombre AS modelo_nombre,
                           u.nombre_completo AS propietario_nombre,
                           u.id_usuario AS id_propietario,
                           a.autoriza_soporte
                      FROM vehiculos v
                      LEFT JOIN modelos_vehiculo m ON v.id_modelo = m.id_modelo
                      LEFT JOIN asignaciones_vehiculo a ON v.id_vehiculo = a.id_vehiculo AND a.estado = 'ACTIVA'
                      LEFT JOIN usuarios u ON a.id_usuario = u.id_usuario
                """
                if user and user["rol"] == "USUARIO":
                    query += " WHERE a.id_usuario = %s AND v.activo = 1 ORDER BY v.id_vehiculo ASC"
                    cur.execute(query, (user["id_usuario"],))
                elif user and user["rol"] == "INVITADO":
                    query += " WHERE v.estado_comercial = 'EXHIBICION' AND v.activo = 1 ORDER BY v.id_vehiculo ASC"
                    cur.execute(query)
                else:
                    query += " WHERE v.activo = 1 ORDER BY v.id_vehiculo ASC"
                    cur.execute(query)
                return cur.fetchall()

    def crear_unidad_fisica(self, id_modelo: int, numero_serie: str, estado_comercial: str,
                             nombre: str, descripcion: str, microcontrolador: str) -> int:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO vehiculos (id_modelo, numero_serie, estado_comercial, nombre, descripcion, microcontrolador, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, 1)
                """, (id_modelo, numero_serie, estado_comercial, nombre, descripcion, microcontrolador))
                vid = cur.lastrowid
                
                # Crear automáticamente estado inicial detenido
                cur.execute("""
                    INSERT INTO estado_vehiculo (id_vehiculo, id_comando, conectado)
                    VALUES (%s, NULL, 0)
                    ON DUPLICATE KEY UPDATE conectado = 0
                """, (vid,))
                conn.commit()
                return vid

    # --- ASIGNACIONES DE VEHÍCULOS ---
    def obtener_asignaciones(self) -> list:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT a.id_asignacion, a.id_usuario, a.id_vehiculo,
                           u.nombre_completo AS cliente_nombre, u.email AS cliente_email,
                           v.nombre AS vehiculo_nombre, v.numero_serie,
                           a.fecha_asignacion, a.estado, a.autoriza_soporte
                      FROM asignaciones_vehiculo a
                      JOIN usuarios u ON a.id_usuario = u.id_usuario
                      JOIN vehiculos v ON a.id_vehiculo = v.id_vehiculo
                     ORDER BY a.id_asignacion DESC
                """)
                return cur.fetchall()

    def asignar_vehiculo(self, id_usuario: int, id_vehiculo: int, autoriza_soporte: bool = False) -> int:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # 1. Finalizar asignaciones activas previas de este vehículo
                cur.execute("""
                    UPDATE asignaciones_vehiculo SET estado = 'FINALIZADA'
                     WHERE id_vehiculo = %s AND estado = 'ACTIVA'
                """, (id_vehiculo,))
                
                # 2. Insertar nueva asignación
                cur.execute("""
                    INSERT INTO asignaciones_vehiculo (id_usuario, id_vehiculo, estado, autoriza_soporte)
                    VALUES (%s, %s, 'ACTIVA', %s)
                """, (id_usuario, id_vehiculo, int(autoriza_soporte)))
                asig_id = cur.lastrowid

                # 3. Marcar vehículo como VENDIDO
                cur.execute("""
                    UPDATE vehiculos SET estado_comercial = 'VENDIDO' WHERE id_vehiculo = %s
                """, (id_vehiculo,))
                conn.commit()
                return asig_id

    def toggle_autorizacion_soporte(self, id_vehiculo: int, id_usuario: int, autoriza: bool):
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE asignaciones_vehiculo
                       SET autoriza_soporte = %s
                     WHERE id_vehiculo = %s AND id_usuario = %s AND estado = 'ACTIVA'
                """, (int(autoriza), id_vehiculo, id_usuario))
                conn.commit()

    # --- SESIONES DE INVITADO ---
    def crear_reserva_invitado(self, id_usuario: int, id_vehiculo: int, minutos: int = 3) -> dict:
        token = secrets.token_hex(20)
        ahora = datetime.now(timezone.utc)
        fin = ahora + timedelta(minutes=minutos)

        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Cancelar sesiones anteriores activas de este vehículo
                cur.execute("""
                    UPDATE sesiones_invitado SET estado = 'CANCELADA'
                     WHERE id_vehiculo = %s AND estado = 'ACTIVA'
                """, (id_vehiculo,))

                cur.execute("""
                    INSERT INTO sesiones_invitado (id_usuario_invitado, id_vehiculo, token_sesion, inicio, fin_programado, estado)
                    VALUES (%s, %s, %s, %s, %s, 'ACTIVA')
                """, (id_usuario, id_vehiculo, token, ahora, fin))
                sesion_id = cur.lastrowid
                conn.commit()

                return {
                    "id_sesion": sesion_id,
                    "id_vehiculo": id_vehiculo,
                    "token_sesion": token,
                    "inicio": ahora,
                    "fin_programado": fin,
                    "segundos_restantes": minutos * 60,
                    "mensaje": f"Sesión de prueba reservada por {minutos} minutos."
                }

    def obtener_sesion_activa_vehiculo(self, id_vehiculo: int) -> dict:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM sesiones_invitado
                     WHERE id_vehiculo = %s AND estado = 'ACTIVA' AND fin_programado > NOW()
                     ORDER BY id_sesion DESC LIMIT 1
                """, (id_vehiculo,))
                return cur.fetchone()

    # --- BITÁCORA DE AUDITORÍA ---
    def registrar_auditoria(self, id_usuario: int, accion: str, entidad: str,
                            id_entidad: int = None, detalle: dict = None, ip_origen: str = "127.0.0.1"):
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                detalle_str = json.dumps(detalle, default=str) if detalle else None
                cur.execute("""
                    INSERT INTO bitacora_auditoria (id_usuario, accion, entidad_afectada, id_entidad, detalle_json, ip_origen)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (id_usuario, accion, entidad, id_entidad, detalle_str, ip_origen))
                conn.commit()

    def obtener_bitacora(self, limite: int = 50) -> list:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT b.id_bitacora, b.id_usuario, u.nombre_completo AS usuario_nombre,
                           b.accion, b.entidad_afectada, b.id_entidad, b.detalle_json,
                           b.ip_origen, b.fecha_hora
                      FROM bitacora_auditoria b
                      LEFT JOIN usuarios u ON b.id_usuario = u.id_usuario
                     ORDER BY b.id_bitacora DESC
                     LIMIT %s
                """, (limite,))
                return cur.fetchall()

    # --- MÉTRICAS DE DASHBOARD ---
    def obtener_metricas_dashboard(self) -> dict:
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) AS total FROM modelos_vehiculo WHERE activo = 1")
                total_modelos = cur.fetchone()["total"]

                cur.execute("SELECT COUNT(*) AS total FROM vehiculos WHERE activo = 1")
                total_unidades = cur.fetchone()["total"]

                cur.execute("SELECT COUNT(*) AS total FROM vehiculos WHERE estado_comercial = 'VENDIDO'")
                unidades_vendidas = cur.fetchone()["total"]

                cur.execute("SELECT COUNT(*) AS total FROM vehiculos WHERE estado_comercial = 'EXHIBICION'")
                unidades_exhibicion = cur.fetchone()["total"]

                cur.execute("SELECT COUNT(*) AS total FROM vehiculos WHERE estado_comercial = 'DISPONIBLE'")
                unidades_disponibles = cur.fetchone()["total"]

                cur.execute("SELECT COUNT(*) AS total FROM usuarios WHERE id_role = 2")
                total_clientes = cur.fetchone()["total"]

                cur.execute("SELECT COUNT(*) AS total FROM historial_comandos")
                total_movimientos = cur.fetchone()["total"]

                cur.execute("SELECT COUNT(*) AS total FROM demos WHERE activo = 1")
                total_demos = cur.fetchone()["total"]

                return {
                    "total_modelos": total_modelos,
                    "total_unidades": total_unidades,
                    "unidades_vendidas": unidades_vendidas,
                    "unidades_exhibicion": unidades_exhibicion,
                    "unidades_disponibles": unidades_disponibles,
                    "total_clientes": total_clientes,
                    "total_movimientos_historial": total_movimientos,
                    "demos_totales": total_demos
                }

admin_repo = AdminRepository()
