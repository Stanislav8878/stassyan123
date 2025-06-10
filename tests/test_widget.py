import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Maestro 1234567812345678", "Maestro 1234 56** **** 5678"),
        ("Счет 123", "Счет **123"),  # короткий счет
        ("Карта 123", "Карта 123"),  # короткий номер карты
        ("", ""),  # пустая строка
    ],
)
def test_mask_account_card(input_str, expected):
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2023-01-15T12:30:00", "15.01.2023"),
        ("2022-12-31T23:59:59", "31.12.2022"),
        ("", ""),  # пустая строка
        ("2023-01", "2023-01"),  # неполная дата
    ],
)
def test_get_date(date_str, expected):
    assert get_date(date_str) == expected
