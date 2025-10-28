import hashlib
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Tuple,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request


def universal_list_key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Optional[Request] = None,
    response: Optional[Any] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    """
    Формирует уникальный ключ кэша, игнорирует session.
    """

    exclude_types = (AsyncSession,)
    cache_kw = {k: v for k, v in kwargs.items() if not isinstance(v, exclude_types)}

    path = request.scope.get("path", "") if request else ""
    method = request.scope.get("method", "GET") if request else ""

    key_str = f"{func.__module__}:{func.__name__}:{method}:{path}:{cache_kw}"
    cache_key = hashlib.md5(key_str.encode()).hexdigest()

    return f"{namespace}:{cache_key}"


def get_by_name_key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Optional[Request] = None,
    response: Optional[Any] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    """
    Формирует уникальный ключ кэша для метода get_by_name.
    Учитывает имя товара и тип ресурса, игнорируя AsyncSession.
    """

    exclude_types = (AsyncSession,)
    filtered_kwargs = {
        k: v for k, v in kwargs.items() if not isinstance(v, exclude_types)
    }

    name_param = next((v for k, v in filtered_kwargs.items() if "name" in k), None)

    if name_param is None:
        raise ValueError("Не найден параметр 'name' в запросе")

    path = request.scope.get("path", "") if request else ""
    method = request.scope.get("method", "GET") if request else ""

    key_str = f"{func.__module__}:{func.__name__}:{method}:{path}:{name_param}"
    cache_key = hashlib.md5(key_str.encode()).hexdigest()

    return f"{namespace}:{cache_key}"


def get_by_id_key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Optional[Request] = None,
    response: Optional[Any] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    """
    Формирует уникальный ключ кэша для метода get_by_id.
    Учитывает id товара и тип ресурса.
    """

    exclude_types = (AsyncSession,)
    filtered_kwargs = {
        k: v for k, v in kwargs.items() if not isinstance(v, exclude_types)
    }

    id_param = next((v for k, v in filtered_kwargs.items() if "id" in k), None)

    if id_param is None:
        raise ValueError("Не найден параметр 'id' в запросе")

    path = request.scope.get("path", "") if request else ""
    method = request.scope.get("method", "GET") if request else ""

    key_str = f"{func.__module__}:{func.__name__}:{method}:{path}:{id_param}"
    cache_key = hashlib.md5(key_str.encode()).hexdigest()

    return f"{namespace}:{cache_key}"
