import re
from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(payment_info: str) -> str:
    """Функция для маскировки номеров карт и счетов"""
    if not payment_info.strip():
        return ""

    numbers = re.findall(r"\d+", payment_info)
    if not numbers:
        return payment_info.strip()

    number = "".join(numbers)

    bank_part = re.sub(r"\d+", "", payment_info).strip()

    if "счет" in payment_info.lower():
        masked = get_mask_account(number)
        return f"{bank_part} {masked}"
    else:
        masked = get_mask_card_number(number)
        return f"{bank_part} {masked}"


def get_date(date_str: str) -> str:
    """Функция для форматирования даты"""
    if not date_str.strip():
        return ""

    try:

        dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y")
    except ValueError:

        return date_str.strip()


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(get_date("2024-03-11T02:26:18.671407"))
