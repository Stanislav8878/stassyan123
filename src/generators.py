from __future__ import annotations

import datetime
from functools import wraps
from typing import Any, Callable, Optional, TypeVar, Iterator, Iterable, Dict

T = TypeVar("T")


def log(filename: Optional[str] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Декоратор для логирования вызовов функций.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            try:
                result = func(*args, **kwargs)
                message = f"{timestamp} - {func_name} ok\n"
                _log_message(message, filename)
                return result
            except Exception as e:
                message = f"{timestamp} - {func_name} error: {type(e).__name__}. " f"Inputs: {args}, {kwargs}\n"
                _log_message(message, filename)
                raise

        return wrapper

    return decorator


def _log_message(message: str, filename: Optional[str] = None) -> None:
    """Внутренняя функция для логирования сообщения."""
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message)
    else:
        print(message, end="")


def filter_by_currency(transactions: Iterable[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по указанной валюте.
    """
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: Iterable[Dict[str, Any]]) -> Iterator[str]:
    """
    Генерирует описания транзакций.
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера карт в формате "XXXX XXXX XXXX XXXX".
    """
    for num in range(start, end + 1):
        yield f"{num:016d}"[:4] + " " + f"{num:016d}"[4:8] + " " + f"{num:016d}"[8:12] + " " + f"{num:016d}"[12:16]