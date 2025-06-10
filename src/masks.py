def get_mask_card_number(card_number: str) -> str:
    """Функция которая принимает на вход номер карты и возвращает ее маску"""
    card_number = card_number.replace(" ", "")
    if len(card_number) < 8 or not card_number.isdigit():
        return card_number
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""
    account_number = account_number.replace(" ", "")
    return f"**{account_number[-4:]}"


if __name__ == "__main__":
    masked_card = get_mask_card_number("1234567812345678")
    print(masked_card)
    print(get_mask_account("123456"))
