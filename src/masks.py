from typing import Union


# Запускаем функцию с аргументом
def get_mask_card_number(card_number: str) -> str:
    """Функция, которая принимает на вход номер карты и возвращает ее маску"""
    if not card_number:
        return ""

    card_number = card_number.replace(" ", "")
    if len(card_number) < 8:
        return card_number

    masked = card_number[:6] + "*" * (len(card_number) - 10) + card_number[-4:]
    return " ".join([masked[i : i + 4] for i in range(0, len(masked), 4)])


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""
    if not account_number:
        return "**"

    account_number = account_number.replace(" ", "")
    if len(account_number) < 4:
        return f"**{account_number}"

    return f"**{account_number[-4:]}"


if __name__ == "__main__":
    masked_card = get_mask_card_number("1234567812345678")
    print(masked_card)
    print(get_mask_account("123456"))
