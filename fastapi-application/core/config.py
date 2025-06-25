from typing import Literal
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    """Конфигурация запуска"""
    host: str = "0.0.0.1"
    port: int = 8000


class ApiPrefix(BaseModel):
    """Конфигурация префикса API"""
    prefix: str = "/api"


class Settings(BaseSettings):
    """Настройка приложения"""

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()

    # Проверка-что MODE одно из этих состояний
    MODE: Literal["DEV", "TEST", "PROD"]

    # Данные для базы данных PostgreSQL
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Данные для тестовой базы данных PostgreSQL
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def TEST_DATABASE_URL(self):
        return (f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@" +
                f"{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}")

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()