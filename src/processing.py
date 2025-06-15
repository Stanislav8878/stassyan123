from __future__ import annotations

from collections import Counter
from datetime import datetime
import re
from typing import Any, Dict, List, Optional


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует транзакции по указанному статусу."""
    return [t for t in transactions if isinstance(t, dict) and str(t.get("state", "")).upper() == str(state).upper()]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате."""

    def get_date(item: Dict[str, Any]) -> datetime:
        """Вспомогательная функция для извлечения даты."""
        date_str = item.get("date", "")
        try:
            return datetime.fromisoformat(date_str) if date_str else datetime.min
        except (ValueError, TypeError):
            return datetime.min

    return sorted([t for t in transactions if isinstance(t, dict)], key=get_date, reverse=reverse)


def search_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по строке в описании с использованием регулярных выражений.

    Args:
        transactions: Список транзакций
        search_string: Строка для поиска в описании

    Returns:
        Список транзакций, где в описании найдена строка поиска
    """
    if not search_string:
        return []

    try:
        pattern = re.compile(search_string, re.IGNORECASE)
        return [t for t in transactions if isinstance(t, dict) and pattern.search(t.get("description", ""))]
    except re.error:
        return []


def count_transactions_by_category(
    transactions: List[Dict[str, Any]], categories: Optional[List[str]] = None
) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по категориям.

    Args:
        transactions: Список транзакций
        categories: Список категорий для подсчета (если None, считает все категории)

    Returns:
        Словарь с количеством транзакций по каждой категории
    """
    descriptions = [str(t.get("description", "UNKNOWN")) for t in transactions if isinstance(t, dict)]

    if categories:
        # Фильтруем только указанные категории
        categories_set = set(categories)
        descriptions = [d for d in descriptions if d in categories_set]

    return dict(Counter(descriptions))
