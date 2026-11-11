from app.core.database import db_manager

class HistorialRepository:
    """Encapsula los 2 Stored Procedures de Historial."""
    
    def registrar(self, id_vehiculo: int, id_comando: int, origen: str, connection=None):
        # SP 12: sp_registrar_historial
        if connection:
            with connection.cursor() as cursor:
                cursor.callproc("sp_registrar_historial", (id_vehiculo, id_comando, origen))
                while cursor.nextset():
                    pass
        else:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.callproc("sp_registrar_historial", (id_vehiculo, id_comando, origen))
                    while cursor.nextset():
                        pass
                    conn.commit()

    def obtener_historial(self, id_vehiculo: int, limite: int = 10) -> list:
        # SP 13: sp_obtener_historial
        with db_manager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_historial", (id_vehiculo,))
                registros = cursor.fetchall()
                # Regla de negocio: Devolver como máximo los 10 más recientes
                return registros[:limite]
