"""
Временный скрипт для проверки чтения CSV-файла.
Можно удалить после проверки.
"""

from src.file_reader import read_transactions_from_csv


def test_csv_reading():
    """Проверяет чтение CSV-файла и вывод данных."""
    print("\n" + "=" * 60)
    print("📁 ПРОВЕРКА ЧТЕНИЯ CSV-ФАЙЛА")
    print("=" * 60)

    file_path = "data/transactions.csv"
    print(f"\n📌 Чтение файла: {file_path}")

    try:
        transactions = read_transactions_from_csv(file_path)
        print(f"\n✅ Успешно загружено {len(transactions)} транзакций")

        if transactions:
            print("\n📊 Первая транзакция:")
            print("-" * 40)
            for key, value in transactions[0].items():
                print(f"   {key}: {value}")

            print("\n📊 Доступные поля:")
            print(f"   {list(transactions[0].keys())}")

            print("\n📊 Все транзакции:")
            print("-" * 40)
            for i, t in enumerate(transactions, 1):
                print(
                    f"{i}. {t.get('date', '')} - {t.get('description', '')} - {t.get('amount', '')} {t.get('currency_name', '')} - {t.get('state', '')}")

        return transactions

    except FileNotFoundError:
        print(f"\n❌ Ошибка: Файл {file_path} не найден!")
        print("   Проверьте, что файл существует в папке data/")
        return []
    except Exception as e:
        print(f"\n❌ Ошибка при чтении CSV: {e}")
        return []


def test_filter_by_state(transactions):
    """Проверяет фильтрацию по статусу."""
    print("\n" + "=" * 60)
    print("🔍 ПРОВЕРКА ФИЛЬТРАЦИИ ПО СТАТУСУ")
    print("=" * 60)

    from src.processing import filter_by_state

    if not transactions:
        print("\n❌ Нет транзакций для фильтрации")
        return

    print(f"\n📌 Всего транзакций: {len(transactions)}")

    # Проверка статусов в данных
    states = set()
    for t in transactions:
        state = t.get("state", "Нет статуса")
        states.add(state)
        print(f"   - {t.get('description', '')}: {state}")

    print(f"\n📌 Доступные статусы: {list(states)}")

    # Фильтрация по EXECUTED
    executed = filter_by_state(transactions, "EXECUTED")
    print(f"\n📌 Транзакции со статусом 'EXECUTED': {len(executed)}")
    for t in executed:
        print(f"   - {t.get('description', '')}")

    # Фильтрация по CANCELED
    canceled = filter_by_state(transactions, "CANCELED")
    print(f"\n📌 Транзакции со статусом 'CANCELED': {len(canceled)}")
    for t in canceled:
        print(f"   - {t.get('description', '')}")


def test_print_transactions(transactions):
    """Проверяет вывод транзакций."""
    print("\n" + "=" * 60)
    print("🖨️ ПРОВЕРКА ВЫВОДА ТРАНЗАКЦИЙ")
    print("=" * 60)

    from src.processing import filter_by_state
    from src.filters import search_transactions

    if not transactions:
        print("\n❌ Нет транзакций для вывода")
        return

    # Фильтруем только EXECUTED
    executed = filter_by_state(transactions, "EXECUTED")

    print(f"\n📌 Вывод {len(executed)} транзакций:")
    print("-" * 40)

    for t in executed:
        date = t.get("date", "")
        description = t.get("description", "")
        amount = t.get("amount", "")
        currency = t.get("currency_name", "")

        # Форматируем дату
        if date and "-" in date:
            parts = date.split("-")
            if len(parts) == 3:
                date = f"{parts[2]}.{parts[1]}.{parts[0]}"

        print(f"{date} {description}")
        print(f"Сумма: {amount} {currency}")
        print()


def main():
    """Главная функция теста."""
    print("\n" + "=" * 60)
    print("🧪 ЗАПУСК ТЕСТА ЧТЕНИЯ CSV")
    print("=" * 60)

    # Шаг 1: Чтение CSV
    transactions = test_csv_reading()

    if not transactions:
        print("\n❌ Тест не пройден: транзакции не загружены")
        return

    # Шаг 2: Проверка фильтрации
    test_filter_by_state(transactions)

    # Шаг 3: Проверка вывода
    test_print_transactions(transactions)

    print("\n" + "=" * 60)
    print("✅ ТЕСТ ЗАВЕРШЕН")
    print("=" * 60)
    print("\n💡 Если транзакции отображаются корректно - программа работает!")
    print("💡 Если есть ошибки - проверьте структуру CSV-файла.")


if __name__ == "__main__":
    main()