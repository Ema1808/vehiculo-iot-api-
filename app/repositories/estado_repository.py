from app.core.database import db_manager

class EstadoRepository:
    """Encapsula los 2 Stored Procedures de Estado."""
    
    def actualizar_estado(self, id_vehiculo: int, id_comando: int, conectado: bool, connection=None):
        # SP 10: sp_actualizar_estado
        if connection:
            with connection.cursor() as cursor:
                cursor.callproc("sp_actualizar_estado", (id_vehiculo, id_comando, conectado))
                while cursor.nextset():
                    pass
        else:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.callproc("sp_actualizar_estado", (id_vehiculo, id_comando, conectado))
                    while cursor.nextset():
                        pass
                    conn.commit()

    def obtener_estado(self, id_vehiculo: int) -> dict:
        # SP 11: sp_obtener_estado
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_estado", (id_vehiculo,))
                return cursor.fetchone()
