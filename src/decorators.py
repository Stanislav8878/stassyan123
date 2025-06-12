from __future__ import annotations

import datetime
import logging
from functools import wraps
from typing import Callable, Optional, TypeVar

T = TypeVar("T")

# Настройка логгера
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def log(
    filename: Optional[str] = None, log_errors: bool = True, log_success: bool = True, log_level: str = "INFO"
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Декоратор для логирования вызовов функций.

    Args:
        filename: Путь к файлу для логирования (None - вывод в консоль)
        log_errors: Логировать ошибки (по умолчанию True)
        log_success: Логировать успешные вызовы (по умолчанию True)
        log_level: Уровень логирования ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            func_name = func.__qualname__

            try:
                result = func(*args, **kwargs)
                if log_success:
                    message = f"{func_name} - Args: {args}, Kwargs: {kwargs} | Result: {result}"
                    _log_message(message, filename, log_level)
                return result
            except Exception as e:
                if log_errors:
                    message = f"{func_name} - {type(e).__name__}: {str(e)} Args: {args}, Kwargs: {kwargs}"
                    _log_message(message, filename, "ERROR")
                raise

        return wrapper

    return decorator


def _log_message(message: str, filename: Optional[str] = None, level: str = "INFO") -> None:
    """Вспомогательная функция для логирования сообщений."""
    try:
        log_level = getattr(logging, level.upper(), logging.INFO)

        if filename:
            with open(filename, "a", encoding="utf-8") as f:
                log_msg = f"{datetime.datetime.now().isoformat()} - {level} - {message}"
                f.write(log_msg + "\n")
        else:
            logger.log(log_level, message)
    except Exception as e:
        logger.error(f"Logging failed: {str(e)}")
