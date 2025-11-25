from pydantic import BaseModel, ConfigDict


class BaseSchemaModel(BaseModel):
    """Базовая схема модели Pydantic."""

    model_config = ConfigDict(from_attributes=True)
