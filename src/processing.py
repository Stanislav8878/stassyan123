from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Улучшенная фильтрация с проверкой структуры данных
    """
    if not transactions or not isinstance(transactions, list):
        return []

    return [t for t in transactions if isinstance(t, dict) and t.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Улучшенная сортировка с обработкой ошибок формата даты
    """

    def get_date(transaction: Dict[str, Any]) -> datetime:
        date_str = transaction.get("date", "")
        try:
            return datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            return datetime.min

    return sorted(transactions, key=get_date, reverse=reverse)
