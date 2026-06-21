import pandas as pd

data = {
    'id': [1, 2, 3, 4, 5],
    'date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
    'amount': [150.50, 45.00, 1200.00, 89.99, 300.00],
    'category': ['Food', 'Transport', 'Salary', 'Entertainment', 'Utilities'],
    'description': ['Grocery shopping', 'Bus ticket', 'Monthly salary', 'Cinema', 'Electricity bill']
}

df = pd.DataFrame(data)
df.to_excel('data/transactions_excel.xlsx', index=False)
print('✅ Excel файл создан!')
