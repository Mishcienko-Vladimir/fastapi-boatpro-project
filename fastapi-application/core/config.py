from typing import Literal
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    """Конфигурация запуска"""
    host: str = "127.0.0.1"
    port: int = 8000


class ApiPrefix(BaseModel):
    """Конфигурация префикса API"""
    prefix: str = "/api"


class Settings(BaseSettings):
    """Настройка приложения"""

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()

    # Данные для базы данных PostgreSQL
#     DB_HOST: str
#     DB_PORT: int
#     DB_USER: str
#     DB_PASS: str
#     DB_NAME: str
#
#     @property
#     def DATABASE_URL(self):
#         return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
#
#
#     model_config = SettingsConfigDict(env_file=".env")
#
settings = Settings()