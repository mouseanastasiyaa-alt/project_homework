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
