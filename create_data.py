"""
Скрипт для создания тестовых данных с разными статусами.
Запустите один раз для обновления CSV и XLSX файлов.
"""

import pandas as pd
import random
from datetime import datetime, timedelta

print("🔄 Создание тестовых данных...")

data = []
statuses = ['EXECUTED', 'CANCELED', 'PENDING']
currencies = ['руб.', 'USD', 'EUR', 'GBP', 'CNY', 'Sol', 'Peso', 'Rupiah']
descriptions = ['Перевод на карту', 'Оплата услуг', 'Перевод организации',
                'Покупка в магазине', 'Открытие вклада', 'Перевод со счета на счет',
                'Оплата связи', 'Перевод на счет']

for i in range(1000):
    date = datetime.now() - timedelta(days=random.randint(1, 2000))
    data.append({
        'id': i + 1,
        'state': random.choice(statuses),
        'date': date.strftime('%Y-%m-%d'),
        'amount': round(random.uniform(100, 50000), 2),
        'currency_name': random.choice(currencies),
        'from': f'Счет {random.randint(1000000000000000, 9999999999999999)}',
        'to': f'Счет {random.randint(1000000000000000, 9999999999999999)}',
        'description': random.choice(descriptions)
    })

df = pd.DataFrame(data)

# Сохраняем CSV
df.to_csv('data/transactions.csv', index=False)
print(f'✅ CSV сохранен: {len(df)} транзакций')

# Сохраняем XLSX
df.to_excel('data/transactions_excel.xlsx', index=False)
print('✅ XLSX сохранен')

# Статистика
print('\n📊 Статистика по статусам:')
print(f'   EXECUTED: {len(df[df["state"] == "EXECUTED"])}')
print(f'   CANCELED: {len(df[df["state"] == "CANCELED"])}')
print(f'   PENDING:  {len(df[df["state"] == "PENDING"])}')

print('\n📊 Примеры валют:')
print(df['currency_name'].value_counts().head(5))

print('\n✅ Готово! Теперь можно запускать python main.py')
