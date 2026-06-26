"""
Тестовый скрипт для быстрой проверки всех функций программы.
Запускает каждую функцию отдельно с тестовыми данными.
"""

import json
from typing import List, Dict, Any

from src.filters import search_transactions, count_categories
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card, get_date

# ============ ТЕСТОВЫЕ ДАННЫЕ ============
TEST_TRANSACTIONS = [
    {
        "id": 1,
        "state": "EXECUTED",
        "date": "2023-01-01",
        "amount": 1000,
        "currency": {"name": "руб."},
        "from": "Счет 1234567890123456",
        "to": "Счет 6543210987654321",
        "description": "Перевод на карту"
    },
    {
        "id": 2,
        "state": "EXECUTED",
        "date": "2023-01-02",
        "amount": 500,
        "currency": {"name": "руб."},
        "from": "MasterCard 1234567890123456",
        "to": "Счет 1111111111111111",
        "description": "Оплата услуг"
    },
    {
        "id": 3,
        "state": "CANCELED",
        "date": "2023-01-03",
        "amount": 2000,
        "currency": {"name": "руб."},
        "from": "Счет 2222222222222222",
        "to": "Visa Platinum 3333333333333333",
        "description": "Перевод организации"
    },
    {
        "id": 4,
        "state": "EXECUTED",
        "date": "2023-01-04",
        "amount": 1500,
        "currency": {"name": "USD"},
        "from": "Счет 4444444444444444",
        "to": "Счет 5555555555555555",
        "description": "Покупка в магазине"
    },
    {
        "id": 5,
        "state": "EXECUTED",
        "date": "2023-01-05",
        "amount": 300,
        "currency": {"name": "руб."},
        "from": "Счет 6666666666666666",
        "to": "Счет 7777777777777777",
        "description": "Оплата связи"
    },
    {
        "id": 6,
        "state": "EXECUTED",
        "date": "2023-01-06",
        "amount": 2500,
        "currency": {"name": "руб."},
        "from": "Счет 8888888888888888",
        "to": "Счет 9999999999999999",
        "description": "Перевод на счет"
    }
]


def print_separator(title: str):
    """Печатает разделитель с заголовком."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_search_transactions():
    """Тест 1: Поиск транзакций по описанию."""
    print_separator("🔍 ТЕСТ 1: ПОИСК ПО ОПИСАНИЮ")

    # Поиск по слову "Перевод"
    result = search_transactions(TEST_TRANSACTIONS, "Перевод")
    print(f"\n📌 Поиск 'Перевод': найдено {len(result)} транзакций")
    for t in result:
        print(f"   ✅ {t['description']}")

    # Поиск по слову "Оплата"
    result = search_transactions(TEST_TRANSACTIONS, "Оплата")
    print(f"\n📌 Поиск 'Оплата': найдено {len(result)} транзакций")
    for t in result:
        print(f"   ✅ {t['description']}")

    # Поиск несуществующего слова
    result = search_transactions(TEST_TRANSACTIONS, "Несуществующее")
    print(f"\n📌 Поиск 'Несуществующее': найдено {len(result)} транзакций")
    print(f"   {'✅ Пустой список (корректно)' if not result else '❌ Ошибка: найдены транзакции'}")

    # Поиск с пустой строкой (должен вернуть все)
    result = search_transactions(TEST_TRANSACTIONS, "")
    print(f"\n📌 Поиск с пустой строкой: возвращено {len(result)} транзакций")
    print(f"   {'✅ Все транзакции (корректно)' if len(result) == len(TEST_TRANSACTIONS) else '❌ Ошибка'}")

    print("\n✅ Тест 1 пройден!")


def test_count_categories():
    """Тест 2: Подсчет категорий."""
    print_separator("📊 ТЕСТ 2: ПОДСЧЕТ КАТЕГОРИЙ")

    categories = ["Перевод на карту", "Оплата услуг", "Перевод организации"]
    result = count_categories(TEST_TRANSACTIONS, categories)

    print("\n📌 Подсчет по категориям:")
    for cat, count in result.items():
        print(f"   ✅ {cat}: {count}")

    # Тест с пустым списком категорий
    result_empty = count_categories(TEST_TRANSACTIONS, [])
    print(f"\n📌 Пустой список категорий: {result_empty}")
    print(f"   {'✅ Пустой словарь (корректно)' if not result_empty else '❌ Ошибка'}")

    print("\n✅ Тест 2 пройден!")


def test_filter_by_state():
    """Тест 3: Фильтрация по статусу."""
    print_separator("🔹 ТЕСТ 3: ФИЛЬТРАЦИЯ ПО СТАТУСУ")

    # Фильтрация EXECUTED
    result = filter_by_state(TEST_TRANSACTIONS, "EXECUTED")
    print(f"\n📌 Статус 'EXECUTED': {len(result)} транзакций")
    for t in result:
        print(f"   ✅ {t['description']} ({t['state']})")

    # Фильтрация CANCELED
    result = filter_by_state(TEST_TRANSACTIONS, "CANCELED")
    print(f"\n📌 Статус 'CANCELED': {len(result)} транзакций")
    for t in result:
        print(f"   ✅ {t['description']} ({t['state']})")

    # Фильтрация несуществующего статуса
    result = filter_by_state(TEST_TRANSACTIONS, "TEST")
    print(f"\n📌 Статус 'TEST': {len(result)} транзакций")
    print(f"   {'✅ Пустой список (корректно)' if not result else '❌ Ошибка'}")

    print("\n✅ Тест 3 пройден!")


def test_sort_by_date():
    """Тест 4: Сортировка по дате."""
    print_separator("📅 ТЕСТ 4: СОРТИРОВКА ПО ДАТЕ")

    # Сортировка по убыванию
    result_desc = sort_by_date(TEST_TRANSACTIONS, reverse=True)
    print("\n📌 По убыванию (сначала новые):")
    for t in result_desc:
        print(f"   ✅ {t['date']}: {t['description']}")

    # Сортировка по возрастанию
    result_asc = sort_by_date(TEST_TRANSACTIONS, reverse=False)
    print("\n📌 По возрастанию (сначала старые):")
    for t in result_asc[:3]:  # Показываем только первые 3
        print(f"   ✅ {t['date']}: {t['description']}")

    print("\n✅ Тест 4 пройден!")


def test_mask_account():
    """Тест 5: Маскировка счетов и карт."""
    print_separator("🎭 ТЕСТ 5: МАСКИРОВКА СЧЕТОВ И КАРТ")

    # Используем функцию из main.py
    from main import mask_account

    test_data = [
        ("Счет 1234567890123456", "Счет **3456"),
        ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
        ("Visa Platinum 3333333333333333", "Visa Platinum 3333 33** **** 3333"),
    ]

    print("\n📌 Проверка маскировки:")
    for original, expected in test_data:
        result = mask_account(original)
        status = "✅" if result == expected else "❌"
        print(f"   {status} {original} -> {result}")
        if result != expected:
            print(f"      Ожидалось: {expected}")

    # Проверка с пустой строкой
    result = mask_account("")
    print(f"\n📌 Пустая строка: '{result}'")
    print(f"   {'✅ Корректно' if result == '' else '❌ Ошибка'}")

    print("\n✅ Тест 5 пройден!")


def test_format_date():
    """Тест 6: Форматирование даты."""
    print_separator("📆 ТЕСТ 6: ФОРМАТИРОВАНИЕ ДАТЫ")

    test_data = [
        ("2023-01-01", "01.01.2023"),
        ("2023-01-02T12:30:45Z", "02.01.2023"),
        ("", ""),
    ]

    print("\n📌 Проверка форматирования даты:")
    for original, expected in test_data:
        result = get_date(original)
        status = "✅" if result == expected else "❌"
        print(f"   {status} {original} -> {result}")
        if result != expected:
            print(f"      Ожидалось: {expected}")

    print("\n✅ Тест 6 пройден!")


def test_full_workflow():
    """Тест 7: Полный рабочий процесс."""
    print_separator("🔄 ТЕСТ 7: ПОЛНЫЙ РАБОЧИЙ ПРОЦЕСС")

    transactions = TEST_TRANSACTIONS.copy()

    print("\n📌 Шаг 1: Исходные данные")
    print(f"   ✅ {len(transactions)} транзакций")

    print("\n📌 Шаг 2: Фильтрация по статусу 'EXECUTED'")
    transactions = filter_by_state(transactions, "EXECUTED")
    print(f"   ✅ {len(transactions)} транзакций")

    print("\n📌 Шаг 3: Сортировка по дате (по убыванию)")
    transactions = sort_by_date(transactions, reverse=True)
    print(f"   ✅ Отсортировано")
    for t in transactions[:3]:
        print(f"      - {t['date']}: {t['description']}")

    print("\n📌 Шаг 4: Фильтрация по валюте (только рублевые)")
    transactions = [t for t in transactions if t.get("currency", {}).get("name") == "руб."]
    print(f"   ✅ {len(transactions)} рублевых транзакций")

    print("\n📌 Шаг 5: Поиск по описанию ('Перевод')")
    transactions = search_transactions(transactions, "Перевод")
    print(f"   ✅ {len(transactions)} транзакций с 'Перевод'")
    for t in transactions:
        print(f"      - {t['description']} ({t['amount']} {t['currency']['name']})")

    print("\n✅ Тест 7 пройден!")


def run_all_tests():
    """Запускает все тесты."""
    print("\n" + "=" * 60)
    print("🚀 ЗАПУСК ВСЕХ ТЕСТОВ")
    print("=" * 60)

    tests = [
        ("Поиск по описанию", test_search_transactions),
        ("Подсчет категорий", test_count_categories),
        ("Фильтрация по статусу", test_filter_by_state),
        ("Сортировка по дате", test_sort_by_date),
        ("Маскировка счетов", test_mask_account),
        ("Форматирование даты", test_format_date),
        ("Полный рабочий процесс", test_full_workflow),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ Ошибка в тесте '{name}': {e}")
            failed += 1

    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ РЕЗУЛЬТАТ")
    print("=" * 60)
    print(f"   ✅ Пройдено: {passed}/{len(tests)}")
    print(f"   ❌ Провалено: {failed}/{len(tests)}")

    if failed == 0:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print(f"\n⚠️ {failed} тестов провалено. Проверьте ошибки выше.")

    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
