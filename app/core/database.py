import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from app.core.config import settings

class DatabaseManager:
    """Clase POO encargada de la conexión segura y ejecución en Amazon RDS."""
    
    def __init__(self):
        self.host = settings.DB_HOST
        self.port = settings.DB_PORT
        self.user = settings.DB_USER
        self.password = settings.DB_PASSWORD
        self.db = settings.DB_NAME

    @contextmanager
    def get_connection(self):
        connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db,
            cursorclass=DictCursor,
            autocommit=False
        )
        try:
            yield connection
        finally:
            connection.close()

db_manager = DatabaseManager()
