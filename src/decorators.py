from __future__ import annotations

import logging
from functools import wraps
from logging import Handler
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def log(
    filename: str | None = None, log_errors: bool = True, log_success: bool = True
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Декоратор для логирования вызовов функций.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Удаляем существующие обработчики
    for h in logger.handlers[:]:
        logger.removeHandler(h)

    # Создаем новый обработчик
    if filename:
        handler: Handler = logging.FileHandler(filename)
    else:
        handler: Handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            func_name = func.__qualname__
            try:
                result = func(*args, **kwargs)
                if log_success:
                    logger.info(f"{func_name} - Args: {args}, Kwargs: {kwargs} | Result: {result}")
                return result
            except Exception as e:
                if log_errors:
                    logger.error(f"{func_name} - {type(e).__name__}: {str(e)} Args: {args}, Kwargs: {kwargs}")
                raise

        return wrapper

    return decorator
