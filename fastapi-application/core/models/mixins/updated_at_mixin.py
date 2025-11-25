from datetime import datetime, UTC

from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped


class UpdatedAtMixin:
    """Миксин, добавляющий поле `updated_at` — дата и время последнего обновления записи."""

    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(tz=UTC).replace(tzinfo=None),
        onupdate=lambda: datetime.now(tz=UTC).replace(tzinfo=None),
        server_default=func.now(),
        server_onupdate=func.now(),
        comment="Последнее обновление записи",
    )
