import pytest
from src.processing import (
    filter_by_state,
    sort_by_date,
    search_by_description,
    count_transactions_by_category,
)


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15", "description": "Перевод организации",
         "operationAmount": {"amount": "100", "currency": {"code": "RUB"}}},
        {"id": 2, "state": "CANCELED", "date": "2023-01-14", "description": "Перевод со счета на счет",
         "operationAmount": {"amount": "200", "currency": {"code": "USD"}}},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-16", "description": "Открытие вклада",
         "operationAmount": {"amount": "300", "currency": {"code": "EUR"}}},
        {"id": 4, "state": "PENDING", "date": "2023-01-13", "description": "Перевод организации",
         "operationAmount": {"amount": "400", "currency": {"code": "RUB"}}},
    ]


def test_search_by_description(sample_transactions):
    # Поиск точного совпадения
    result = search_by_description(sample_transactions, "Перевод организации")
    assert len(result) == 2
    assert all(t["description"] == "Перевод организации" for t in result)

    # Поиск с регистронезависимостью
    result = search_by_description(sample_transactions, "ОТКРЫТИЕ")
    assert len(result) == 1
    assert result[0]["description"] == "Открытие вклада"

    # Поиск с регулярным выражением
    result = search_by_description(sample_transactions, "Перевод.*")
    assert len(result) == 3

    # Пустой поиск
    result = search_by_description(sample_transactions, "")
    assert len(result) == 0

    # Несуществующий поиск
    result = search_by_description(sample_transactions, "Несуществующее описание")
    assert len(result) == 0


def test_count_transactions_by_category(sample_transactions):
    # Подсчет всех категорий
    result = count_transactions_by_category(sample_transactions)
    assert result == {
        "Перевод организации": 2,
        "Перевод со счета на счет": 1,
        "Открытие вклада": 1,
    }

    # Подсчет только указанных категорий
    result = count_transactions_by_category(sample_transactions, ["Перевод организации"])
    assert result == {"Перевод организации": 2}

    # Подсчет несуществующей категории
    result = count_transactions_by_category(sample_transactions, ["Несуществующая категория"])
    assert result == {}