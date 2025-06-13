# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
import re
from typing import Any, Final, Optional, Union

# Константы
MIN_ACCOUNT_DIGITS: Final[int] = 4
MIN_CARD_DIGITS: Final[int] = 8
MASK_PREFIX: Final[str] = "**"
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"


def setup_logger() -> logging.Logger:
    """Настройка логгера для модуля."""
    logger = logging.getLogger("masks")
    logger.setLevel(logging.DEBUG)

    # Очистка предыдущих обработчиков
    logger.handlers = []

    handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

    logger.addHandler(handler)
    return logger


logger = setup_logger()


def extract_digits(text: str) -> str:
    """Извлекает цифры из строки."""
    return re.sub(r"\D", "", text)


def get_mask_card_number(card_number: Optional[Union[str, int, Any]]) -> str:
    """Маскирует номер банковской карты."""
    if card_number is None:
        logger.warning("Получен None вместо номера карты")
        return ""

    if not isinstance(card_number, (str, int)):
        logger.warning(f"Неверный тип номера карты: {type(card_number)}")
        return ""

    card_str = str(card_number)
    cleaned = card_str.strip()
    if not cleaned:
        logger.warning("Пустая строка номера карты")
        return ""

    digits = extract_digits(cleaned)
    if len(digits) < MIN_CARD_DIGITS or not digits.isdigit():
        logger.warning(f"Некорректный номер карты: {cleaned}")
        return cleaned

    return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"


def get_mask_account(account_number: Optional[Union[str, int, Any]]) -> str:
    """Маскирует номер банковского счета."""
    if account_number is None:
        logger.warning("Получен None вместо номера счета")
        return ""

    if not isinstance(account_number, (str, int)):
        logger.warning(f"Неверный тип номера счета: {type(account_number)}")
        return "**"

    account_str = str(account_number)
    cleaned = account_str.strip()
    if not cleaned:
        logger.warning("Пустая строка номера счета")
        return "**"

    digits = extract_digits(cleaned)
    if not digits:
        logger.warning("Номер счета не содержит цифр")
        return f"**{cleaned}" if cleaned else "**"

    if len(digits) < MIN_ACCOUNT_DIGITS:
        logger.warning(f"Номер счета слишком короткий: {digits}")
        return f"**{digits}"

    return f"**{digits[-MIN_ACCOUNT_DIGITS:]}"
