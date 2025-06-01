from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(name_card: [str]) -> [str]:
    """Функция, которая принимает один аргумент — строку, содержащую тип и номер карты или счета,
    возвращать строку с замаскированным номером."""
    if "счет" in name_card.lower():

        number_card = name_card[-20:]

        masked_card = get_mask_account(number_card)
        return f"Счет {masked_card}"
    else:
        name_card_bank = name_card[-16:]
        masked_visa = get_mask_card_number(name_card_bank)
        name_bank = name_card[:-16]
        return f"{name_bank} {masked_visa}"


print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Счет 73654108430135874305"))


def get_date(data_card_number: [str]) -> str:
    '''Функция, которая принимает на вход строку с датой в одном
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ"'''
    data_correct = data_card_number[8:10] + "." + data_card_number[5:7] + "." + data_card_number[:4]
    return data_correct


print(get_date("2024-03-11T02:26:18.671407"))