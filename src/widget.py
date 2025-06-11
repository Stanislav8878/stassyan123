from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

from decorators import log
from masks import get_mask_account, get_mask_card_number


@log(filename="widget_operations.log")
def mask_account_card(payment_info: Optional[str]) -> str:
    """Улучшенная маскировка платежной информации."""
    if not payment_info or not isinstance(payment_info, str):
        return ""

    cleaned_info = payment_info.strip()
    if not cleaned_info:
        return ""

    numbers = re.findall(r"\d+", cleaned_info)
    if not numbers:
        return cleaned_info

    number = "".join(numbers)
    bank_part = re.sub(r"\d+", "", cleaned_info).strip()

    if "счет" in cleaned_info.lower():
        masked = get_mask_account(number)
    else:
        masked = get_mask_card_number(number)

    return f"{bank_part} {masked}" if bank_part else masked


def get_date(date_str: Optional[str]) -> str:
    """Форматирование даты с улучшенной обработкой ошибок."""
    if not date_str or not isinstance(date_str, str):
        return ""

    cleaned_date = date_str.strip()
    if not cleaned_date:
        return ""

    try:
        dt = datetime.strptime(cleaned_date[:10], "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return cleaned_date
