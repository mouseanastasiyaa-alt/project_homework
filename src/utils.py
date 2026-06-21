"""
Модуль с вспомогательными утилитами для работы с данными.
"""

import json
import os
from typing import Any, Dict, List


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с данными

    Raises:
        FileNotFoundError: Если файл не найден
        json.JSONDecodeError: Если файл содержит некорректный JSON

    Example:
        >>> data = read_json_file("data/operations.json")
        >>> print(len(data))
        10
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями

    Raises:
        FileNotFoundError: Если файл не найден
        json.JSONDecodeError: Если файл содержит некорректный JSON

    Example:
        >>> transactions = load_transactions_from_json("data/operations.json")
        >>> print(len(transactions))
        10
    """
    return read_json_file(file_path)


def filter_transactions_by_state(
    transactions: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу выполнения.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций
        state (str): Статус для фильтрации (по умолчанию "EXECUTED")

    Returns:
        List[Dict[str, Any]]: Отфильтрованный список транзакций

    Example:
        >>> filtered = filter_transactions_by_state(transactions, "CANCELED")
        >>> print(len(filtered))
        3
    """
    return [tx for tx in transactions if tx.get("state") == state]
