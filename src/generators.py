from typing import Dict, Iterator, List, Union


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]:
    """
    Фильтрует транзакции по заданной валюте и возвращает итератор.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, "USD")

    Yields:
        Словарь транзакции, где валюта операции соответствует заданной
    """
    for transaction in transactions:
        op_amount = transaction.get("operationAmount", {})
        curr = op_amount.get("currency", {}).get("code")
        if curr == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """
    Генерирует описания транзакций по очереди.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        Описание очередной транзакции
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера карт в заданном диапазоне.

    Args:
        start: Начальный номер карты
        end: Конечный номер карты (включительно)

    Yields:
        Номер карты в формате XXXX XXXX XXXX XXXX
    """
    for num in range(start, end + 1):
        yield f"{num:016d}"[:4] + " " + f"{num:016d}"[4:8] + " " + \
            f"{num:016d}"[8:12] + " " + f"{num:016d}"[12:16]