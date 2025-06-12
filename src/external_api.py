import os
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными о транзакции

    Returns:
        Сумма в рублях (float) или None в случае ошибки
    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"]

        if currency == "RUB":
            return amount

        # Получаем курс валют
        response = requests.get(BASE_URL, params={"base": currency, "symbols": "RUB"}, headers={"apikey": API_KEY})
        response.raise_for_status()

        rate = response.json()["rates"]["RUB"]
        return amount * rate
    except (KeyError, ValueError, requests.RequestException):
        return None
