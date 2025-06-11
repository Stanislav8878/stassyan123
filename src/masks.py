from __future__ import annotations

import re


def get_mask_card_number(card_number: str) -> str:
    """
    Улучшенная маскировка номера карты с валидацией.

    Формат: XXXX XX** **** XXXX
    """
    if not card_number or not isinstance(card_number, str):
        return card_number or ""

    digits = re.sub(r"\D", "", card_number)

    if len(digits) < 8 or not digits.isdigit():
        return card_number

    return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Улучшенная маскировка счета с валидацией.

    Формат: **XXXX
    """
    if not account_number or not isinstance(account_number, str):
        return account_number or ""

    digits = re.sub(r"\D", "", account_number)

    if not digits:
        return "**"

    return f"**{digits[-4:]}" if len(digits) >= 4 else f"**{digits}"
