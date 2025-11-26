from typing import Type, Any
from fastapi import Form
from pydantic import BaseModel, ValidationError
from inspect import signature, Parameter


def create_multipart_form_data(model: Type[BaseModel]):
    """
    Создаёт зависимость FastAPI для парсинга `multipart/form-data` в указанную Pydantic-модель.

    Используется для унификации создания продуктов (прицепов, моторов, катеров) через
    админ-панель и API, избегая дублирования `Form(...)` вручную.

    Особенности:
        - Поддерживает все типы полей Pydantic: str, int, bool, float, Enum, Optional
        - Учитывает `default`, `default_factory` (через модель), `description`
        - Автоматически генерирует OpenAPI-документацию
        - Работает с валидацией на уровне Pydantic
        - Не обрабатывает файлы — файлы должны передаваться отдельно через `File(...)`

    Example:
        @router.post("/")
        async def create_trailer(
            session: Annotated[AsyncSession, Depends(get_db_session)],
            trailer_data: Annotated[TrailerCreate, Depends(create_multipart_form_data(TrailerCreate))],
            images: Annotated[list[UploadFile], File(..., description="Изображения товара")],
        ) -> TrailerRead:
        ...

    Args:
        model (Type[BaseModel]): Pydantic-модель создания товара, например TrailerCreate.

    Raises:
        ValidationError: HTTP 422 - если данные из формы не проходят валидацию по схеме модели.

    Returns:
        Callable[..., BaseModel]: Возвращает экземпляр `model` с данными из формы.
    """

    def dependency(**form_data: Any) -> BaseModel:
        try:
            return model(**form_data)
        except ValidationError as exc:
            raise ValidationError(model.__name__, exc.errors())

    # Динамически устанавливаем сигнатуру
    fields = model.model_fields
    sig = {}
    for name, field in fields.items():
        default = ... if field.is_required() else field.default
        description = field.description or f"Поле {name}"
        sig[name] = Parameter(
            name=name,
            kind=Parameter.KEYWORD_ONLY,
            default=Form(default, description=description),
            annotation=field.annotation,
        )

    dependency.__signature__ = signature(dependency).replace(
        parameters=list(sig.values())
    )
    return dependency
