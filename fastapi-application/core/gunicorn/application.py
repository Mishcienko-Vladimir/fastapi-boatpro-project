from fastapi import FastAPI
from gunicorn.app.base import BaseApplication


class Application(BaseApplication):
    """Для запуска приложения через gunicorn"""

    def __init__(self, application: FastAPI, options: dict | None = None):
        self.options = options or {}
        self.application = application
        super().__init__()

    def load(self):
        """Загрузка приложения"""
        return self.application

    @property
    def config_options(self) -> dict:
        """Проверяет есть ли ключ"""
        return {
            k: v
            for k, v in self.options.items()
            if k in self.cfg.settings and v is not None
        }

    def load_config(self):
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)
