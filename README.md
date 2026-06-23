# Проект Домашних Заданий (project_homework)

Этот проект содержит модули для обработки транзакций, маскирования карт и счетов.

## Тестирование

Для автоматической проверки работоспособности функций используется библиотека `pytest`.

### Запуск всех тестов
```bash
pytest
```

### Генерация отчета о покрытии (Coverage)
```bash
pytest --cov=src --cov-report=term-missing
```

### HTML отчет
Для создания папки с визуальным отчетом покрытия в формате HTML:
```bash
pytest --cov=src --cov-report=html
```

## Модуль генераторов (src/generators.py)

Модуль предназначен для эффективной "ленивой" обработки данных транзакций без перегрузки оперативной памяти.

### Примеры использования функций:

1. **Фильтрация по валюте (`filter_by_currency`)**:
```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions_list, "USD")
for tx in usd_transactions:
    print(tx)
```

2. **Получение описаний (`transaction_descriptions`)**:
```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions_list)
print(next(descriptions))
```

3. **Генератор номеров карт (`card_number_generator`)**:
```python
from src.generators import card_number_generator

for card in card_number_generator(1, 5):
    print(card)  # Формат: 0000 0000 0000 0001
```

## Модуль декораторов (src/decorators.py)

Модуль содержит универсальный декоратор `@log`, который автоматически регистрирует детали выполнения функций.

### Пример использования:

```python
from src.decorators import log

# Логирование в консоль
@log()
def my_function(x, y):
    return x + y

# Логирование в файл
@log(filename="mylog.txt")
def another_function():
    pass
```
## Модуль чтения файлов (src/file_reader.py)

Модуль предназначен для чтения финансовых транзакций из файлов форматов CSV и Excel (XLSX).

### Функции:

1. **`read_transactions_from_csv(file_path: str)`** - Чтение транзакций из CSV-файла

2. **`read_transactions_from_excel(file_path: str)`** - Чтение транзакций из Excel-файла

### Параметры:
- `file_path` (str): Путь к файлу с данными

### Возвращаемое значение:
- `List[Dict[str, Any]]`: Список словарей, где каждый словарь представляет одну транзакцию

### Исключения:
- `FileNotFoundError`: Если файл не найден
- `ValueError`: Если файл пустой или не содержит данных
- `Exception`: При других ошибках чтения

### Примеры использования:

```python
from src.file_reader import read_transactions_from_csv, read_transactions_from_excel

# Чтение из CSV-файла
transactions_csv = read_transactions_from_csv("data/transactions.csv")
print(f"Загружено {len(transactions_csv)} транзакций из CSV")

# Чтение из Excel-файла
transactions_excel = read_transactions_from_excel("data/transactions_excel.xlsx")
print(f"Загружено {len(transactions_excel)} транзакций из Excel")

# Обработка данных
for transaction in transactions_csv:
    print(f"ID: {transaction['id']}, Сумма: {transaction['amount']}")

## Новая функциональность (homework_13_2)

### 🔍 Поиск транзакций по описанию
Добавлена функция `search_transactions()`, которая позволяет искать транзакции по строке в описании с использованием регулярных выражений (библиотека `re`).

**Особенности:**
- Регистронезависимый поиск
- Поддержка частичных совпадений
- Возвращает список транзакций, содержащих искомую строку

**Пример использования:**
```python
from src.filters import search_transactions

transactions = [...]  # список транзакций
result = search_transactions(transactions, "Перевод")
# Вернет все транзакции с "Перевод" в описании
