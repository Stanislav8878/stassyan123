from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрация транзакций по статусу с улучшенной проверкой."""
    if not isinstance(transactions, list):
        return []

    valid_state = str(state).upper() if state else "EXECUTED"
    return [t for t in transactions if isinstance(t, dict) and str(t.get("state", "")).upper() == valid_state]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """Сортировка транзакций по дате с улучшенной обработкой ошибок."""
    if not isinstance(transactions, list):
        return []

    def get_date(transaction: Dict[str, Any]) -> datetime:
        date_str = str(transaction.get("date", "")) if transaction else ""
        try:
            return datetime.fromisoformat(date_str) if date_str else datetime.min
        except (ValueError, TypeError):
            return datetime.min

    return sorted([t for t in transactions if isinstance(t, dict)], key=get_date, reverse=reverse)
