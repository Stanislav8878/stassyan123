from __future__ import annotations

import datetime
from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций.

    Args:
        filename: Имя файла для записи логов. Если None, логи выводятся в консоль.

    Returns:
        Декоратор для функции.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Формируем сообщение для логирования
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            try:
                result = func(*args, **kwargs)
                message = f"{timestamp} - {func_name} ok\n"
                log_message(message, filename)
                return result
            except Exception as e:
                message = f"{timestamp} - {func_name} error: {type(e).__name__}. " f"Inputs: {args}, {kwargs}\n"
                log_message(message, filename)
                raise

        return wrapper

    return decorator


def log_message(message: str, filename: Optional[str] = None) -> None:
    """
    Записывает сообщение в файл или выводит в консоль.

    Args:
        message: Сообщение для логирования.
        filename: Имя файла для записи. Если None, выводит в консоль.
    """
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message)
    else:
        print(message, end="")
