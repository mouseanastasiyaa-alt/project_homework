"""
Модуль с генераторами для эффективной обработки транзакций.
"""

from typing import Any, Dict, Generator, List


def filter_by_currency(
        transactions: List[Dict[str, Any]], currency: str
) -> Generator[Dict[str, Any], None, None]:
    """
    Фильтрует транзакции по валюте.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций
        currency (str): Код валюты (например, "USD", "EUR")

    Yields:
        Generator[Dict[str, Any], None, None]: Транзакции с указанной валютой

    Example:
        >>> usd_txs = filter_by_currency(transactions, "USD")
        >>> for tx in usd_txs:
        >>>     print(tx["amount"])
    """
    for transaction in transactions:
        # Проверяем наличие валюты в разных форматах
        if "currency" in transaction and transaction["currency"] == currency:
            yield transaction
        elif "operationAmount" in transaction:
            op_amount = transaction["operationAmount"]
            if isinstance(op_amount, dict):
                currency_info = op_amount.get("currency")
                if isinstance(currency_info, dict):
                    if currency_info.get("code") == currency:
                        yield transaction
                elif currency_info == currency:
                    yield transaction


def transaction_descriptions(
        transactions: List[Dict[str, Any]]
) -> Generator[str, None, None]:
    """
    Генерирует описания транзакций.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций

    Yields:
        Generator[str, None, None]: Описания транзакций

    Example:
        >>> desc = transaction_descriptions(transactions)
        >>> print(next(desc))
        'Grocery shopping'
    """
    for transaction in transactions:
        if "description" in transaction:
            yield transaction["description"]
        elif "desc" in transaction:
            yield transaction["desc"]
        else:
            yield ""


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генерирует номера карт в формате "XXXX XXXX XXXX XXXX".

    Args:
        start (int): Начальный номер
        end (int): Конечный номер (включительно)

    Yields:
        Generator[str, None, None]: Номера карт в формате с пробелами

    Example:
        >>> for card in card_number_generator(1, 3):
        >>>     print(card)
        '0000 0000 0000 0001'
        '0000 0000 0000 0002'
        '0000 0000 0000 0003'
    """
    for num in range(start, end + 1):
        card_str = str(num).zfill(16)
        yield " ".join([card_str[i: i + 4] for i in range(0, 16, 4)])
