from mypy.types import Union


# Запускаем функцию с аргументом
def get_mask_card_number(card_number: Union[str]) -> str:
    """Функция которая принимает на вход номер карты и возвращает ее маску"""

    card_number = card_number.replace(" ", "")
    masked_card_number = " ".join(card_number[i : i + 4] for i in range(0, len(card_number), 4))
    masked_card_number_list = list(masked_card_number)

    for i in range(len(masked_card_number_list)):
        if 7 <= i <= 13 and masked_card_number_list[i] != " ":
            masked_card_number_list[i] = "*"

    masked_card_number = "".join(masked_card_number_list)
    return masked_card_number


# masked_card = get_mask_card_number("1234567812345678")
# print(masked_card)


def get_mask_account(card_number: Union[str]) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""

    card_number = card_number.replace(" ", "")
    last_part = str(card_number[-4:])
    return f"**{last_part}"


# print(get_mask_account("123456"))
