import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_currency(transaction: dict[str, Any]) -> float:
    """Принимает транзакцию и возвращает сумму операции в рублях."""
    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount", "0")
    currency_code = operation_amount.get("currency", {}).get("code", "RUB")

    try:
        amount = float(amount_str)
    except ValueError:
        return 0.0

    if currency_code == "RUB":
        return amount

    if currency_code in ["USD", "EUR"]:
        api_key = os.getenv("API_KEY")
        if not api_key:
            return 0.0

        url = (
            f"https://api.apilayer.com/exchangerates_data/latest"
            f"?base={currency_code}&symbols=RUB"
        )

        headers = {"apikey": api_key}

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                rub_rate = data.get("rates", {}).get("RUB")

                if rub_rate:
                    return amount * float(rub_rate)

        except requests.RequestException:
            return 0.0

    return 0.0
