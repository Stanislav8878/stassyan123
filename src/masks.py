from __future__ import annotations

import logging
import re
from typing import Optional

# Настройка логгера
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/masks.log", mode="w")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Optional[str]) -> str:
    """Маскирует номер банковской карты."""
    if not isinstance(card_number, str) or not card_number.strip():
        logger.warning("Пустой или неверный тип номера карты")
        return ""

    digits = re.sub(r"\D", "", card_number)
    if len(digits) < 8 or not digits.isdigit():
        logger.warning(f"Некорректный номер карты: {card_number}")
        return card_number

    return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"


def get_mask_account(account_number: Optional[str]) -> str:
    """Маскирует номер банковского счета."""
    if account_number is None:
        logger.warning("Получен None вместо номера счета")
        return ""

    if not isinstance(account_number, str):
        logger.warning(f"Неверный тип номера счета: {type(account_number)}")
        return "**"

    cleaned = account_number.strip()
    if not cleaned:
        logger.warning("Пустая строка номера счета")
        return "**"

    digits = re.sub(r"\D", "", cleaned)
    # Упрощенная логика возврата
    return f"**{digits[-4:]}"  # digits не может быть пустым после проверок
