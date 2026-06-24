"""
Главный модуль программы для работы с банковскими транзакциями.

Обеспечивает пользовательский интерфейс для работы с транзакциями из разных источников:
JSON, CSV и XLSX файлов. Позволяет фильтровать, сортировать и анализировать транзакции.
"""

import json
from typing import List, Dict, Any

# Импортируем наши модули
from src.file_reader import read_transactions_from_csv, read_transactions_from_excel
from src.filters import search_transactions
from src.processing import filter_by_state, sort_by_date


def get_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает транзакции из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict[str, Any]]: Список транзакций.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                print("Ошибка: Файл должен содержать список транзакций.")
                return []
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
        return []
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат JSON-файла.")
        return []


def get_valid_status() -> str:
    """
    Запрашивает у пользователя статус операции и проверяет его корректность.

    Returns:
        str: Корректный статус операции.
    """
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        status = input(
            "\nВведите статус, по которому необходимо выполнить фильтрацию.\nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n").strip().upper()

        if status in valid_statuses:
            print(f"Операции отфильтрованы по статусу \"{status}\"")
            return status
        else:
            print(f"Статус операции \"{status}\" недоступен.")


def get_user_choice(prompt: str) -> bool:
    """
    Запрашивает у пользователя ответ на вопрос с вариантами да/нет.

    Args:
        prompt (str): Текст вопроса.

    Returns:
        bool: True если пользователь ответил "да", False если "нет".
    """
    while True:
        answer = input(f"{prompt} Да/Нет\n").strip().lower()
        if answer in ["да", "lf", "yes", "y"]:
            return True
        elif answer in ["нет", "ytn", "no", "n"]:
            return False
        else:
            print("Пожалуйста, введите 'Да' или 'Нет'")


def get_sort_order() -> str:
    """
    Запрашивает у пользователя порядок сортировки.

    Returns:
        str: 'asc' для возрастания, 'desc' для убывания.
    """
    while True:
        order = input("\nОтсортировать по возрастанию или по убыванию?\n").strip().lower()
        if order in ["по возрастанию", "возрастанию", "возрастание", "asc", "возраст"]:
            return "asc"
        elif order in ["по убыванию", "убыванию", "убывание", "desc", "убыв"]:
            return "desc"
        else:
            print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """
    Выводит список транзакций в формате, соответствующем заданию.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций.
    """
    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}")
    print()

    for transaction in transactions:
        # Получаем данные
        date = transaction.get("date", "")
        description = transaction.get("description", "Описание не указано")
        from_account = transaction.get("from", "")
        to_account = transaction.get("to", "")
        amount = transaction.get("amount", "0")

        # Получаем валюту
        currency = transaction.get("currency", {})
        if isinstance(currency, dict):
            currency_name = currency.get("name", "")
        else:
            currency_name = str(currency)

        # Если валюты нет, пробуем поле currency_name
        if not currency_name:
            currency_name = transaction.get("currency_name", "руб.")

        # Форматируем дату из YYYY-MM-DD в DD.MM.YYYY
        if date and isinstance(date, str) and "-" in date:
            try:
                parts = date.split("-")
                if len(parts) == 3:
                    date = f"{parts[2]}.{parts[1]}.{parts[0]}"
            except:
                pass

        # Маскируем счета
        def mask_account(account: str) -> str:
            """Маскирует номер счета (показывает только последние 4 цифры)."""
            if not account:
                return ""
            if "Счет" in account:
                parts = account.split()
                if len(parts) >= 2:
                    number = parts[-1]
                    if len(number) >= 4:
                        return f"Счет **{number[-4:]}"
            return account

        from_masked = mask_account(from_account)
        to_masked = mask_account(to_account)

        # Выводим в требуемом формате
        print(f"{date} {description}")

        if from_masked and to_masked:
            print(f"{from_masked} -> {to_masked}")
        elif from_masked:
            print(from_masked)
        elif to_masked:
            print(to_masked)

        print(f"Сумма: {amount} {currency_name}")
        print()


def main() -> None:
    """
    Главная функция программы. Реализует пользовательский интерфейс.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Шаг 1: Выбор источника данных
    print("\nВыберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("\nВаш выбор (1, 2 или 3): ").strip()

        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            file_path = "data/operations.json"  # Путь к JSON файлу
            transactions = get_transactions_from_json(file_path)
            break
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            file_path = "data/transactions.csv"  # Путь к CSV файлу
            try:
                transactions = read_transactions_from_csv(file_path)
                print(f"Успешно загружено {len(transactions)} транзакций из CSV")
            except Exception as e:
                print(f"Ошибка при чтении CSV: {e}")
                transactions = []
            break
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            file_path = "data/transactions_excel.xlsx"  # Путь к вашему XLSX файлу
            try:
                transactions = read_transactions_from_excel(file_path)
                print(f"Успешно загружено {len(transactions)} транзакций из XLSX")
            except Exception as e:
                print(f"Ошибка при чтении XLSX: {e}")
                transactions = []
            break
        else:
            print("Пожалуйста, введите 1, 2 или 3")

    if not transactions:
        print("Не удалось загрузить транзакции. Программа завершает работу.")
        return

    # Шаг 2: Фильтрация по статусу
    status = get_valid_status()
    transactions = filter_by_state(transactions, status)

    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Шаг 3: Сортировка по дате
    if get_user_choice("Отсортировать операции по дате?"):
        order = get_sort_order()
        transactions = sort_by_date(transactions, reverse=(order == "desc"))

    # Шаг 4: Фильтрация по валюте
    if get_user_choice("Выводить только рублевые транзакции?"):
        transactions = [t for t in transactions if t.get("currency", {}).get("name") == "руб."]

    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Шаг 5: Поиск по описанию
    if get_user_choice("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска: ").strip()
        transactions = search_transactions(transactions, search_word)

    # Шаг 6: Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")
    print_transactions(transactions)


if __name__ == "__main__":
    main()
