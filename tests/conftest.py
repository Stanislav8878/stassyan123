import pytest

@pytest.fixture
def card_numbers():
    return [
        "1234567812345678",
        "1111222233334444",
        "5555666677778888",
        "1234 5678 1234 5678"
    ]

@pytest.fixture
def accounts():
    return [
        "12345678901234567890",
        "98765432109876543210",
        "1234"
    ]

@pytest.fixture
def transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T12:30:00"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-14T11:20:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-16T10:10:00"},
        {"id": 4, "state": "PENDING", "date": "2023-01-13T09:05:00"}
    ]