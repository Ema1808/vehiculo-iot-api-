from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str = "vehiculo_iot"

    # Configuración de Seguridad y JWT
    JWT_SECRET_KEY: str = "iot_jwt_super_secret_key_2026_emmanuel_tecnm"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    PASSWORD_SALT: str = "iot_salt_2026_"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
