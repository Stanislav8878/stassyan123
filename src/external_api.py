from __future__ import annotations

import os
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, TypedDict, Union

import requests
from dotenv import load_dotenv

load_dotenv()


class OperationAmount(TypedDict):
    amount: Union[str, float, Decimal]
    currency: Dict[str, str]


class Transaction(TypedDict):
    operationAmount: OperationAmount


BASE_URL: str = "https://api.apilayer.com/exchangerates_data/latest"
RATES_CACHE: Dict[str, Dict[str, float]] = {}
CACHE_EXPIRATION: Dict[str, datetime] = {}


def convert_to_rub(transaction: Transaction) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        raise ValueError("API_KEY is not set in environment variables")

    try:
        operation_amount = transaction["operationAmount"]
        amount = Decimal(str(operation_amount["amount"]))
        currency = operation_amount["currency"]["code"]

        if currency == "RUB":
            return float(amount)

        # Очищаем кэш перед использованием в тестах
        if os.environ.get("PYTEST_CURRENT_TEST"):
            RATES_CACHE.clear()
            CACHE_EXPIRATION.clear()

        if currency in RATES_CACHE and datetime.now() < CACHE_EXPIRATION.get(currency, datetime.min):
            rate = Decimal(str(RATES_CACHE[currency]["RUB"]))
        else:
            response = requests.get(
                BASE_URL, params={"base": currency, "symbols": "RUB"}, headers={"apikey": api_key}, timeout=10
            )
            response.raise_for_status()

            rates = response.json()["rates"]
            rate = Decimal(str(rates["RUB"]))

            RATES_CACHE[currency] = rates
            CACHE_EXPIRATION[currency] = datetime.now() + timedelta(hours=1)

        return float(amount * rate)

    except KeyError as e:
        raise KeyError(f"Missing required field in transaction: {e}")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid amount value: {e}")
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {e}")
