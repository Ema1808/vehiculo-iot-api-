from app.core.database import db_manager

class ComandoRepository:
    """Encapsula los 4 Stored Procedures de Comandos."""
    
    def crear(self, id_vehiculo: int, nombre: str, codigo: int, descripcion: str) -> int:
        # SP 6: sp_crear_comando
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_crear_comando", (id_vehiculo, nombre, codigo, descripcion))
                result = cursor.fetchone()
                conn.commit()
                return result["id_comando"] if result else None

    def obtener_por_vehiculo(self, id_vehiculo: int) -> list:
        # SP 7: sp_obtener_comandos_vehiculo
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_comandos_vehiculo", (id_vehiculo,))
                return cursor.fetchall()

    def actualizar(self, id_comando: int, nombre: str, codigo: int, descripcion: str, activo: bool):
        # SP 8: sp_actualizar_comando
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_actualizar_comando", (id_comando, nombre, codigo, descripcion, activo))
                conn.commit()

    def eliminar(self, id_comando: int):
        # SP 9: sp_eliminar_comando
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_eliminar_comando", (id_comando,))
                conn.commit()
