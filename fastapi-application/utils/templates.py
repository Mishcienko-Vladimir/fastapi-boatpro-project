from fastapi.templating import Jinja2Templates
from datetime import datetime

from core.config import BASE_DIR


def format_datetime(value: str | datetime) -> str:
    """
    Форматирует дату в формате YYYY-MM-DD HH:MM.
    Поддерживает строки в формате ISO (например, '2025-10-07T12:25:49.158480').
    """
    if isinstance(value, str):
        try:
            # Пробуем преобразовать строку в datetime
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return value  # Возвращаем исходную строку, если не удалось преобразовать
    elif isinstance(value, datetime):
        dt = value
    else:
        return ""

    return dt.strftime("%Y-%m-%d %H:%M")


class AppTemplates(Jinja2Templates):
    """Добавляет дополнительные фильтры для шаблонов Jinja2Templates."""

    def __init__(self, directory):
        super().__init__(directory=directory)
        self.env.filters["format_datetime"] = format_datetime


templates = AppTemplates(directory=BASE_DIR / "templates")
