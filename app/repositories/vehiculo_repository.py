from app.core.database import db_manager

class VehiculoRepository:
    """Encapsula los 5 Stored Procedures de Vehículos."""
    
    def crear(self, nombre: str, modelo: str, descripcion: str, microcontrolador: str) -> int:
        # SP 1: sp_crear_vehiculo
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_crear_vehiculo", (nombre, modelo, descripcion, microcontrolador))
                result = cursor.fetchone()
                conn.commit()
                return result["id_vehiculo"] if result else None

    def obtener_todos(self) -> list:
        # SP 2: sp_obtener_vehiculos
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_vehiculos")
                return cursor.fetchall()

    def obtener_por_id(self, id_vehiculo: int) -> dict:
        # SP 3: sp_obtener_vehiculo
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_vehiculo", (id_vehiculo,))
                return cursor.fetchone()

    def actualizar(self, id_vehiculo: int, nombre: str, modelo: str, descripcion: str, microcontrolador: str, activo: bool):
        # SP 4: sp_actualizar_vehiculo
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_actualizar_vehiculo", (id_vehiculo, nombre, modelo, descripcion, microcontrolador, activo))
                conn.commit()

    def eliminar(self, id_vehiculo: int):
        # SP 5: sp_eliminar_vehiculo
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_eliminar_vehiculo", (id_vehiculo,))
                conn.commit()
