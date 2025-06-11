from __future__ import annotations

import datetime
import logging
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")


def log(
    filename: Optional[str] = None, log_errors: bool = True, log_success: bool = True
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Улучшенный декоратор для логирования с настройками уровней логирования.

    Args:
        filename: Путь к файлу лога (None - вывод в консоль)
        log_errors: Логировать ошибки (по умолчанию True)
        log_success: Логировать успешные вызовы (по умолчанию True)
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            timestamp = datetime.datetime.now().isoformat()
            func_name = func.__name__

            try:
                result = func(*args, **kwargs)
                if log_success:
                    message = f"{timestamp} - INFO - {func_name} - Args: {args}, Kwargs: {kwargs}\n"
                    _log_message(message, filename)
                return result
            except Exception as e:
                if log_errors:
                    message = (
                        f"{timestamp} - ERROR - {func_name} - {type(e).__name__}: {str(e)} "
                        f"Args: {args}, Kwargs: {kwargs}\n"
                    )
                    _log_message(message, filename)
                raise

        return wrapper

    return decorator


def _log_message(message: str, filename: Optional[str] = None) -> None:
    """Улучшенное логирование с проверкой файла"""
    if filename:
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(message)
        except IOError as e:
            logging.error(f"Failed to write log: {str(e)}")
    else:
        print(message, end="")
