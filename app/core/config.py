from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str = "vehiculo_iot"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
