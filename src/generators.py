from typing import Any, Dict, Generator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Generator[Dict[str, Any], None, None]:
    """Фильтрует транзакции по заданной валюте.

    Принимает список словарей с транзакциями и код валюты (например, 'USD').
    Возвращает итератор, который поочередно выдает подходящие транзакции.
    """
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency_info = operation_amount.get("currency", {})
        currency_code = currency_info.get("code")

        if currency_code == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """Принимает список транзакций и возвращает описание каждой операции по очереди.

    Использует yield для генерации значений по запросу аналитика.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX.

    Принимает начальное (start) и конечное (stop) числовые значения диапазона.
    """
    for number in range(start, stop + 1):
        str_number = f"{number:016d}"
        formatted_card = f"{str_number[0:4]} {str_number[4:8]} {str_number[8:12]} {str_number[12:16]}"
        yield formatted_card
