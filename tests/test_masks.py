import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567812345678", "1234 56** **** 5678"),
        ("1111222233334444", "1111 22** **** 4444"),
        ("1234 5678 1234 5678", "1234 56** **** 5678"),
        ("123", "123"),  # короткий номер
        ("", ""),  # пустая строка
        ("abcd", "abcd"),  # не цифры
    ],
)
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account, expected",
    [
        ("12345678901234567890", "**7890"),
        ("98765432109876543210", "**3210"),
        ("1234", "**1234"),
        ("12", "**12"),  # короткий счет
        ("", "**"),  # пустая строка
    ],
)
def test_get_mask_account(account, expected):
    assert get_mask_account(account) == expected
