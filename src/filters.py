"""
Модуль для фильтрации и анализа банковских операций.

Содержит функции для поиска транзакций по описанию с использованием
регулярных выражений и подсчета операций по категориям.
"""

import re
from collections import Counter
from typing import Any, Dict, List


def search_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Поиск транзакций по строке в описании с использованием регулярных выражений.

    Args:
        transactions (List[Dict[str, Any]]): Список словарей с данными о транзакциях.
        search_string (str): Строка для поиска в описании транзакций.

    Returns:
        List[Dict[str, Any]]: Список транзакций, у которых в описании есть искомая строка.
    """
    # Если строка поиска пустая, возвращаем все транзакции
    if not search_string:
        return transactions

    # Создаем список для хранения найденных транзакций
    result = []

    # Проходим по каждой транзакции
    for transaction in transactions:
        # Получаем описание транзакции, если оно есть
        description = transaction.get("description", "")

        # Используем re.search для поиска (регистронезависимый поиск)
        # re.IGNORECASE - флаг для игнорирования регистра
        if re.search(search_string, description, flags=re.IGNORECASE):
            result.append(transaction)

    return result


def count_categories(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчет количества операций в каждой категории.

    Args:
        transactions (List[Dict[str, Any]]): Список словарей с данными о транзакциях.
        categories (List[str]): Список категорий для подсчета.

    Returns:
        Dict[str, int]: Словарь с количеством операций в каждой категории.
    """
    # Создаем объект Counter для подсчета
    category_counter = Counter()

    # Проходим по каждой транзакции
    for transaction in transactions:
        # Получаем описание транзакции
        description = transaction.get("description", "")

        # Проверяем, есть ли описание в списке категорий
        if description in categories:
            # Увеличиваем счетчик для этой категории
            category_counter[description] += 1

    # Преобразуем Counter в обычный словарь и возвращаем
    return dict(category_counter)
