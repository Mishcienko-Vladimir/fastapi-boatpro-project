# Что бы не было двух уровней: from core.models.db_helper import db_helper -> from core.models import db_helper
__all__ = (
    "db_helper",
)

from .db_helper import db_helper