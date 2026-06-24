"""
Главный модуль программы для работы с банковскими транзакциями.
Обеспечивает пользовательский интерфейс для работы с транзакциями из JSON, CSV и XLSX файлов.
"""

import json
from typing import Any, Dict, List

from src.file_reader import read_transactions_from_csv, read_transactions_from_excel
from src.filters import search_transactions
from src.processing import filter_by_state, sort_by_date


def get_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Читает транзакции из JSON-файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка: {e}" if isinstance(e, FileNotFoundError)
              else "Ошибка: Неверный формат JSON")
        return []


def get_valid_status() -> str:
    """Запрашивает у пользователя статус операции."""
    valid = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(
            "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).strip().upper()
        if status in valid:
            print(f"Операции отфильтрованы по статусу \"{status}\"")
            return status
        print(f"Статус операции \"{status}\" недоступен.")


def get_user_choice(prompt: str) -> bool:
    """Запрашивает ответ Да/Нет."""
    while True:
        answer = input(f"{prompt} Да/Нет\n").strip().lower()
        if answer in ["да", "lf", "yes", "y"]:
            return True
        if answer in ["нет", "ytn", "no", "n"]:
            return False
        print("Пожалуйста, введите 'Да' или 'Нет'")


def get_sort_order() -> str:
    """Запрашивает порядок сортировки."""
    while True:
        order = input("\nОтсортировать по возрастанию или по убыванию?\n").strip().lower()
        if order in ["по возрастанию", "возрастанию", "возрастание", "asc", "возраст"]:
            return "asc"
        if order in ["по убыванию", "убыванию", "убывание", "desc", "убыв"]:
            return "desc"
        print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")


def mask_account(account: Any) -> str:
    """Маскирует номер счета или карты."""

    if account is None:
        return ""

    if not isinstance(account, str):
        return ""

    account = account.strip()

    if not account:
        return ""

    parts = account.split()

    if len(parts) < 2:
        return account

    if "Счет" in account:
        return f"Счет **{parts[-1][-4:]}" if len(parts[-1]) >= 4 else account

    card_type = " ".join(parts[:-1])
    number = parts[-1]

    if len(number) >= 16:
        return f"{card_type} {number[:4]} {number[4:6]}** **** {number[-4:]}"

    if len(number) >= 4:
        return f"{card_type} **{number[-4:]}"

    return account


def format_date(date: str) -> str:
    """Форматирует дату из YYYY-MM-DD в DD.MM.YYYY."""
    if not date or not isinstance(date, str):
        return date
    try:
        date_str = date.split("T")[0] if "T" in date else date
        parts = date_str.split("-")
        return f"{parts[2]}.{parts[1]}.{parts[0]}" if len(parts) == 3 else date
    except (ValueError, AttributeError, IndexError):
        return date


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Выводит список транзакций в формате задания."""
    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for t in transactions:
        currency = t.get("currency", {})
        currency_name = currency.get("name", "") if isinstance(currency, dict) else str(currency)
        currency_name = currency_name or t.get("currency_name", "руб.")

        from_masked = mask_account(t.get("from", ""))
        to_masked = mask_account(t.get("to", ""))

        print(f"{format_date(t.get('date', ''))} {t.get('description', 'Описание не указано')}")
        if from_masked and to_masked:
            print(f"{from_masked} -> {to_masked}")
        elif from_masked:
            print(from_masked)
        elif to_masked:
            print(to_masked)
        print(f"Сумма: {t.get('amount', '0')} {currency_name}\n")


def main() -> None:
    """Главная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    print("\nВыберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("\nВаш выбор (1, 2 или 3): ").strip()

        if choice == "1":
            print("\nДля обработки выбран JSON-файл.")
            file_path = "data/operations.json"
            transactions = get_transactions_from_json(file_path)
            break
        elif choice == "2":
            print("\nДля обработки выбран CSV-файл.")
            file_path = "data/transactions.csv"
            try:
                transactions = read_transactions_from_csv(file_path)
                print(f"Успешно загружено {len(transactions)} транзакций из CSV")
            except Exception as e:
                print(f"Ошибка при чтении CSV: {e}")
                transactions = []
            break
        elif choice == "3":
            print("\nДля обработки выбран XLSX-файл.")
            file_path = "data/transactions_excel.xlsx"
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

    status = get_valid_status()
    transactions = filter_by_state(transactions, status)

    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    if get_user_choice("Отсортировать операции по дате?"):
        order = get_sort_order()
        transactions = sort_by_date(transactions, reverse=(order == "desc"))

    if get_user_choice("Выводить только рублевые транзакции?"):
        transactions = [t for t in transactions
                        if t.get("currency", {}).get("name") == "руб."]

    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    if get_user_choice("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска: ").strip()
        transactions = search_transactions(transactions, search_word)

    print("\nРаспечатываю итоговый список транзакций...")
    print_transactions(transactions)


if __name__ == "__main__":
    main()
