"""
Главный модуль программы для работы с банковскими транзакциями.
Обеспечивает пользовательский интерфейс для работы с транзакциями из JSON, CSV и XLSX файлов.
"""

import json
import re
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
        if answer in ["да", "lf", "yes", "y", "д"]:
            return True
        if answer in ["нет", "ytn", "no", "n", "н"]:
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


def get_currency_name(transaction: Dict[str, Any]) -> str:
    """
    Извлекает название валюты из транзакции.
    Поддерживает JSON, CSV и XLSX форматы.
    """
    # 1. Проверяем operationAmount.currency.name (JSON)
    operation_amount = transaction.get("operationAmount")
    if isinstance(operation_amount, dict):
        currency = operation_amount.get("currency")
        if isinstance(currency, dict):
            currency_name = currency.get("name")
            if currency_name:
                return currency_name

    # 2. Проверяем currency (может быть dict или str)
    currency = transaction.get("currency")
    if isinstance(currency, dict):
        currency_name = currency.get("name")
        if currency_name:
            return currency_name
    elif isinstance(currency, str) and currency:
        # Если это код валюты, конвертируем в название
        currency_map = {
            "RUB": "руб.",
            "USD": "USD",
            "EUR": "EUR",
            "GBP": "GBP",
            "CNY": "CNY",
        }
        return currency_map.get(currency.upper(), currency)

    # 3. Проверяем currency_name (CSV)
    currency_name = transaction.get("currency_name")
    if currency_name and isinstance(currency_name, str):
        # Нормализуем название валюты
        if currency_name.lower() in ["руб.", "руб", "рубль", "rur"]:
            return "руб."
        return currency_name

    # 4. Проверяем currency_code (CSV)
    currency_code = transaction.get("currency_code")
    if currency_code and isinstance(currency_code, str):
        currency_map = {
            "RUB": "руб.",
            "USD": "USD",
            "EUR": "EUR",
            "GBP": "GBP",
            "CNY": "CNY",
            "PEN": "PEN",
            "BRL": "BRL",
        }
        return currency_map.get(currency_code.upper(), currency_code)

    # 5. Проверяем поле "Валюта" (Excel)
    currency_name = transaction.get("Валюта")
    if currency_name and isinstance(currency_name, str):
        return currency_name

    # 6. Проверяем поле "amount" - возможно, там есть символ валюты
    amount = transaction.get("amount")
    if isinstance(amount, str):
        if "RUB" in amount or "руб" in amount:
            return "руб."
        if "USD" in amount or "$" in amount:
            return "USD"
        if "EUR" in amount or "€" in amount:
            return "EUR"

    # 7. Если ничего не найдено, возвращаем "руб." по умолчанию
    return "руб."


def get_amount(transaction: Dict[str, Any]) -> str:
    """
    Извлекает сумму из транзакции из разных возможных полей.
    Поддерживает JSON, CSV и XLSX форматы.
    """
    amount = None

    # 1. Проверяем operationAmount.amount (JSON)
    operation_amount = transaction.get("operationAmount")
    if isinstance(operation_amount, dict):
        amount = operation_amount.get("amount")
        if isinstance(amount, (int, float)):
            amount = str(amount)
        elif isinstance(amount, str):
            # Извлекаем только число из строки (если есть валюта)
            match = re.search(r'([\d,]+\.?[\d]*)', amount)
            if match:
                amount = match.group(1).replace(',', '.')

    # 2. Проверяем amount (CSV/JSON)
    if amount is None or amount == "":
        amount = transaction.get("amount")
        if isinstance(amount, (int, float)):
            amount = str(amount)
        elif isinstance(amount, str):
            # Извлекаем только число из строки (если есть валюта)
            match = re.search(r'([\d,]+\.?[\d]*)', amount)
            if match:
                amount = match.group(1).replace(',', '.')

    # 3. Проверяем sum
    if amount is None or amount == "":
        amount = transaction.get("sum")
        if isinstance(amount, (int, float)):
            amount = str(amount)

    # 4. Проверяем Сумма (Excel)
    if amount is None or amount == "":
        amount = transaction.get("Сумма")
        if isinstance(amount, (int, float)):
            amount = str(amount)

    # 5. Проверяем total
    if amount is None or amount == "":
        amount = transaction.get("total")
        if isinstance(amount, (int, float)):
            amount = str(amount)

    # 6. Если ничего не найдено
    if amount is None or amount == "":
        amount = "0"

    amount_str = str(amount)
    # Убираем .0 только если это целое число
    if amount_str.endswith('.0') and len(amount_str) > 2:
        amount_str = amount_str[:-2]

    return amount_str


def fix_csv_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Исправляет структуру транзакций из CSV-файла.
    Нормализует данные и валюту.
    """
    fixed_transactions = []

    for t in transactions:
        fixed_t = dict(t)

        # Нормализуем название валюты
        currency_name = fixed_t.get("currency_name", "")
        if isinstance(currency_name, str):
            currency_lower = currency_name.lower()
            if currency_lower in ["руб.", "руб", "рубль", "rur"]:
                fixed_t["currency_name"] = "руб."
            elif currency_lower in ["usd", "$"]:
                fixed_t["currency_name"] = "USD"
            elif currency_lower in ["eur", "€"]:
                fixed_t["currency_name"] = "EUR"
            elif currency_lower in ["gbp", "£"]:
                fixed_t["currency_name"] = "GBP"

        # Если есть currency_code, но нет currency_name
        if not fixed_t.get("currency_name") and fixed_t.get("currency_code"):
            currency_code = fixed_t["currency_code"]
            if isinstance(currency_code, str):
                currency_map = {
                    "RUB": "руб.",
                    "USD": "USD",
                    "EUR": "EUR",
                    "GBP": "GBP",
                    "CNY": "CNY",
                    "PEN": "Sol",
                    "BRL": "Real",
                }
                code = currency_code.upper()
                fixed_t["currency_name"] = currency_map.get(code, code)

        # Если валюта все еще не определена, ставим "руб."
        if not fixed_t.get("currency_name"):
            fixed_t["currency_name"] = "руб."

        fixed_transactions.append(fixed_t)

    return fixed_transactions


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Выводит список транзакций в формате задания."""
    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for t in transactions:
        currency_name = get_currency_name(t)
        amount_str = get_amount(t)

        from_masked = mask_account(t.get("from", ""))
        to_masked = mask_account(t.get("to", ""))

        # Форматируем дату
        date_str = format_date(t.get('date', ''))
        description = t.get('description', 'Описание не указано')

        print(f"{date_str} {description}")

        if from_masked and to_masked:
            print(f"{from_masked} -> {to_masked}")
        elif from_masked:
            print(from_masked)
        elif to_masked:
            print(to_masked)

        # Выводим сумму с валютой
        if currency_name:
            print(f"Сумма: {amount_str} {currency_name}")
        else:
            print(f"Сумма: {amount_str}")
        print()


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

                # Исправляем структуру CSV-данных
                transactions = fix_csv_transactions(transactions)

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

    # Получаем статус и фильтруем
    status = get_valid_status()
    transactions = filter_by_state(transactions, status)

    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    if get_user_choice("Отсортировать операции по дате?"):
        order = get_sort_order()
        transactions = sort_by_date(transactions, reverse=(order == "desc"))

    # Фильтр по рублевым транзакциям
    if get_user_choice("Выводить только рублевые транзакции?"):
        filtered = []
        for t in transactions:
            currency_name = get_currency_name(t)
            # Проверяем разные варианты написания "рубль"
            if currency_name.lower() in ["руб.", "руб", "rur", "rub", "рубль"]:
                filtered.append(t)
        transactions = filtered
        print(f"Отфильтровано {len(transactions)} рублевых транзакций")

    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Фильтр по слову в описании
    if get_user_choice("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска: ").strip()
        transactions = search_transactions(transactions, search_word)

    print("\nРаспечатываю итоговый список транзакций...")
    print_transactions(transactions)


if __name__ == "__main__":
    main()
