import pytest
import os
from unittest.mock import patch, Mock
from src.external_api import convert_to_rub, RATES_CACHE, CACHE_EXPIRATION

@pytest.fixture
def sample_transaction():
    return {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"}
        }
    }

@pytest.fixture
def rub_transaction():
    return {
        "operationAmount": {
            "amount": "1000",
            "currency": {"code": "RUB"}
        }
    }

@patch('requests.get')
def test_convert_to_rub_usd(mock_get, sample_transaction):
    mock_response = Mock()
    mock_response.json.return_value = {'rates': {'RUB': 75.5}}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Устанавливаем временный API_KEY для теста
    with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
        result = convert_to_rub(sample_transaction)
        assert result == 7550.0
        mock_get.assert_called_once()

def test_convert_to_rub_rub(rub_transaction):
    with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
        assert convert_to_rub(rub_transaction) == 1000.0

@patch('requests.get')
def test_cache_usage(mock_get, sample_transaction):
    # Очищаем кэш перед тестом
    RATES_CACHE.clear()
    CACHE_EXPIRATION.clear()

    mock_response = Mock()
    mock_response.json.return_value = {'rates': {'RUB': 75.5}}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
        # Первый вызов - запрос к API
        result1 = convert_to_rub(sample_transaction)
        assert mock_get.call_count == 1

        # Второй вызов - использование кэша
        result2 = convert_to_rub(sample_transaction)
        assert mock_get.call_count == 1
        assert result1 == result2

def test_invalid_transaction_structure():
    with patch.dict('os.environ', {'EXCHANGE_RATE_API_KEY': 'test_key'}):
        with pytest.raises(KeyError):
            convert_to_rub({})

def test_missing_api_key():
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError):
            convert_to_rub({"operationAmount": {"amount": "100", "currency": {"code": "USD"}}})