"""
Тесты для модуля filters.py.

Проверяет функции поиска транзакций и подсчета категорий.
"""

import pytest
from src.filters import search_transactions, count_categories


# Фикстура с тестовыми данными для всех тестов
@pytest.fixture
def sample_transactions():
    """
    Возвращает список тестовых транзакций для использования в тестах.
    """
    return [
        {
            "id": 1,
            "description": "Перевод на карту",
            "amount": "1000",
            "currency": {"name": "руб."},
            "date": "2023-01-01"
        },
        {
            "id": 2,
            "description": "Оплата услуг связи",
            "amount": "500",
            "currency": {"name": "руб."},
            "date": "2023-01-02"
        },
        {
            "id": 3,
            "description": "Перевод организации",
            "amount": "2000",
            "currency": {"name": "руб."},
            "date": "2023-01-03"
        },
        {
            "id": 4,
            "description": "Покупка в магазине",
            "amount": "1500",
            "currency": {"name": "руб."},
            "date": "2023-01-04"
        },
        {
            "id": 5,
            "description": "Перевод на счет",
            "amount": "3000",
            "currency": {"name": "USD"},
            "date": "2023-01-05"
        }
    ]


# ==================== ТЕСТЫ ДЛЯ search_transactions ====================

def test_search_transactions_found(sample_transactions):
    """
    Тест: Поиск транзакций по существующей строке.
    Должен вернуть список транзакций, содержащих искомую строку.
    """
    result = search_transactions(sample_transactions, "Перевод")

    # Проверяем, что найдены 3 транзакции с "Перевод" в описании
    assert len(result) == 3
    # Проверяем, что все найденные транзакции содержат "Перевод"
    for transaction in result:
        assert "Перевод" in transaction["description"]


def test_search_transactions_not_found(sample_transactions):
    """
    Тест: Поиск транзакций по несуществующей строке.
    Должен вернуть пустой список.
    """
    result = search_transactions(sample_transactions, "Несуществующее")

    # Проверяем, что результат - пустой список
    assert result == []


def test_search_transactions_empty_string(sample_transactions):
    """
    Тест: Поиск с пустой строкой.
    Должен вернуть все транзакции.
    """
    result = search_transactions(sample_transactions, "")

    # Проверяем, что возвращены все транзакции
    assert len(result) == len(sample_transactions)
    assert result == sample_transactions


def test_search_transactions_case_insensitive(sample_transactions):
    """
    Тест: Поиск должен быть регистронезависимым.
    Строки "перевод" и "ПЕРЕВОД" должны давать одинаковый результат.
    """
    result_lower = search_transactions(sample_transactions, "перевод")
    result_upper = search_transactions(sample_transactions, "ПЕРЕВОД")
    result_title = search_transactions(sample_transactions, "Перевод")

    # Все три варианта должны дать одинаковое количество результатов
    assert len(result_lower) == len(result_upper) == len(result_title)
    # Проверяем, что это 3 транзакции
    assert len(result_lower) == 3


def test_search_transactions_partial_match(sample_transactions):
    """
    Тест: Поиск по части слова.
    Должен находить транзакции, содержащие часть слова.
    """
    result = search_transactions(sample_transactions, "связ")

    # Должна найти транзакцию с "связи" в описании
    assert len(result) == 1
    assert result[0]["description"] == "Оплата услуг связи"


def test_search_transactions_empty_list():
    """
    Тест: Поиск в пустом списке.
    Должен вернуть пустой список.
    """
    result = search_transactions([], "Перевод")
    assert result == []


# ==================== ТЕСТЫ ДЛЯ count_categories ====================

def test_count_categories_all_found(sample_transactions):
    """
    Тест: Подсчет категорий, все категории присутствуют.
    """
    categories = ["Перевод на карту", "Оплата услуг связи", "Перевод организации", "Покупка в магазине"]

    result = count_categories(sample_transactions, categories)

    # Проверяем, что все категории посчитаны правильно
    assert result["Перевод на карту"] == 1
    assert result["Оплата услуг связи"] == 1
    assert result["Перевод организации"] == 1
    assert result["Покупка в магазине"] == 1


def test_count_categories_some_found(sample_transactions):
    """
    Тест: Подсчет категорий, только некоторые присутствуют.
    """
    categories = ["Перевод на карту", "Перевод организации", "Несуществующая категория"]

    result = count_categories(sample_transactions, categories)

    # Проверяем, что посчитаны только существующие категории
    assert result["Перевод на карту"] == 1
    assert result["Перевод организации"] == 1
    # Несуществующая категория не должна появиться в результате
    assert "Несуществующая категория" not in result


def test_count_categories_no_matches(sample_transactions):
    """
    Тест: Подсчет категорий, ни одна не совпадает.
    """
    categories = ["Несуществующая", "Другая"]

    result = count_categories(sample_transactions, categories)

    # Должен вернуть пустой словарь
    assert result == {}


def test_count_categories_empty_transactions():
    """
    Тест: Подсчет категорий для пустого списка транзакций.
    """
    categories = ["Перевод на карту", "Оплата услуг связи"]

    result = count_categories([], categories)

    # Должен вернуть пустой словарь
    assert result == {}


def test_count_categories_empty_categories(sample_transactions):
    """
    Тест: Подсчет категорий для пустого списка категорий.
    """
    result = count_categories(sample_transactions, [])

    # Должен вернуть пустой словарь
    assert result == {}


def test_count_categories_duplicates(sample_transactions):
    """
    Тест: Подсчет категорий при наличии дублирующихся описаний.
    Создаем список с повторяющимися транзакциями.
    """
    transactions_with_duplicates = sample_transactions + [
        {
            "id": 6,
            "description": "Перевод на карту",
            "amount": "5000",
            "currency": {"name": "руб."},
            "date": "2023-01-06"
        },
        {
            "id": 7,
            "description": "Перевод на карту",
            "amount": "2500",
            "currency": {"name": "руб."},
            "date": "2023-01-07"
        }
    ]

    categories = ["Перевод на карту", "Оплата услуг связи"]

    result = count_categories(transactions_with_duplicates, categories)

    # Должно быть 3 транзакции "Перевод на карту" (одна изначальная + две добавленные)
    assert result["Перевод на карту"] == 3
    assert result["Оплата услуг связи"] == 1
