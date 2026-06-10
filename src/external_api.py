import os
from typing import Any
import requests


def convert_currency(transaction: dict[str, Any]) -> float:
    """Принимает транзакцию и возвращает сумму операции в рублях (float).

    Если валюта USD или EUR, запрашивает актуальный курс через API.
    """
    # Извлекаем сумму и код валюты из структуры транзакции
    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount", "0")
    currency_code = operation_amount.get("currency", {}).get("code", "RUB")

    # Переводим строку с суммой в число с плавающей точкой
    amount = float(amount_str)

    # Если транзакция уже в рублях, конвертация не требуется
    if currency_code == "RUB":
        return amount

    # Если валюта USD или EUR, обращаемся к внешнему API
    if currency_code in ["USD", "EUR"]:
        # Достаем API-ключ из переменных окружения (.env)
        api_key = os.getenv("API_KEY")
        if not api_key:
            # Если ключа нет, возвращаем 0.0 во избежание падения программы
            return 0.0

        # Формируем URL для запроса (конвертируем из текущей валюты currency_code в RUB)
        url = f"https://apilayer.com{currency_code}&amount={amount}"

        # Передаем API-ключ в заголовках (headers) запроса, как требует документация APILayer
        headers = {"apikey": api_key}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            # Если запрос успешный, извлекаем результат из JSON-ответа
            if response.status_code == 200:
                data = response.json()
                return float(data.get("result", 0.0))
        except requests.RequestException:
            # Если возникли проблемы с сетью или сервером, возвращаем 0.0
            return 0.0

    return 0.0
