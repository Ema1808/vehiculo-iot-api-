from app.core.database import db_manager

class DemoRepository:
    """Encapsula los 8 Stored Procedures de Demos y sus Movimientos."""
    
    def crear_demo(self, id_vehiculo: int, nombre: str, descripcion: str) -> int:
        # SP 14: sp_crear_demo
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_crear_demo", (id_vehiculo, nombre, descripcion))
                res = cursor.fetchone()
                conn.commit()
                return res["id_demo"] if res else None

    def obtener_demos(self, id_vehiculo: int) -> list:
        # SP 15: sp_obtener_demos
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_demos", (id_vehiculo,))
                return cursor.fetchall()

    def actualizar_demo(self, id_demo: int, nombre: str, descripcion: str, activo: bool):
        # SP 16: sp_actualizar_demo
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_actualizar_demo", (id_demo, nombre, descripcion, activo))
                conn.commit()

    def eliminar_demo(self, id_demo: int):
        # SP 17: sp_eliminar_demo
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_eliminar_demo", (id_demo,))
                conn.commit()

    def agregar_movimiento(self, id_demo: int, id_comando: int, orden: int, duracion_ms: int, pausa_ms: int):
        # SP 18: sp_agregar_movimiento_demo
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_agregar_movimiento_demo", (id_demo, id_comando, orden, duracion_ms, pausa_ms))
                conn.commit()

    def obtener_movimientos(self, id_demo: int) -> list:
        # SP 19: sp_obtener_movimientos_demo
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_movimientos_demo", (id_demo,))
                return cursor.fetchall()

    def actualizar_movimiento(self, id_demo_movimiento: int, id_comando: int, orden: int, duracion_ms: int, pausa_ms: int):
        # SP 20: sp_actualizar_movimiento_demo
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_actualizar_movimiento_demo", (id_demo_movimiento, id_comando, orden, duracion_ms, pausa_ms))
                conn.commit()

    def eliminar_movimiento(self, id_demo_movimiento: int):
        # SP 21: sp_eliminar_movimiento_demo
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_eliminar_movimiento_demo", (id_demo_movimiento,))
                conn.commit()
