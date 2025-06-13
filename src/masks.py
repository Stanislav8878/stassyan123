from __future__ import annotations

import logging
import re
from typing import Any, Final, Optional, Union

# Константы
MIN_ACCOUNT_DIGITS: Final[int] = 4
MASK_PREFIX: Final[str] = "**"
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"


def setup_logger() -> logging.Logger:
    """Настройка логгера для модуля."""
    logger = logging.getLogger("masks")
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler("logs/masks.log", mode="w")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

    logger.addHandler(handler)
    return logger


logger = setup_logger()


def extract_digits(text: str) -> str:
    """Извлекает цифры из строки."""
    return re.sub(r"\D", "", text)


def get_mask_account(account_number: Optional[Union[str, int, Any]]) -> str:
    """Маскирует номер банковского счета.

    Args:
        account_number: Номер счета для маскировки (строка, число или None)

    Returns:
        Маскированная строка счета в формате **XXXX
    """
    # Обработка None
    if account_number is None:
        logger.warning("Получен None вместо номера счета")
        return MASK_PREFIX

    # Преобразование в строку
    account_str: str
    if isinstance(account_number, (str, int)):
        account_str = str(account_number)
    else:
        logger.warning(f"Неверный тип номера счета: {type(account_number)}")
        return MASK_PREFIX

    # Очистка строки
    cleaned = account_str.strip()
    if not cleaned:
        logger.warning("Пустая строка номера счета")
        return MASK_PREFIX

    # Извлечение цифр
    digits = extract_digits(cleaned)

    # Обработка результата
    if not digits:
        logger.warning("Номер счета не содержит цифр")
        return MASK_PREFIX

    if len(digits) < MIN_ACCOUNT_DIGITS:
        logger.warning(f"Номер счета слишком короткий: {digits}")
        return f"{MASK_PREFIX}{digits}"

    return f"{MASK_PREFIX}{digits[-MIN_ACCOUNT_DIGITS:]}"
