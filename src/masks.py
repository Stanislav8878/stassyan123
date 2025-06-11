from __future__ import annotations

import re
from typing import Optional


def get_mask_card_number(card_number: Optional[str]) -> str:
    """Маскировка номера карты с улучшенной валидацией."""
    if not card_number or not isinstance(card_number, str):
        return ""

    digits = re.sub(r"\D", "", card_number)
    if len(digits) < 8 or not digits.isdigit():
        return card_number

    return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"


def get_mask_account(account_number: Optional[str]) -> str:
    """Маскировка счета с улучшенной валидацией."""
    if account_number is None:
        return ""

    if not isinstance(account_number, str):
        return "**"

    cleaned = account_number.strip()
    if not cleaned:
        return "**"

    digits = re.sub(r"\D", "", cleaned)
    if not digits:
        return f"**{cleaned}" if cleaned else "**"

    last_digits = digits[-4:] if len(digits) >= 4 else digits
    return f"**{last_digits}"
