from pathlib import Path
from file_handlers import read_csv_file, read_excel_file

# Чтение CSV
csv_transactions = read_csv_file(Path("./data/transactions.csv"))
print("CSV Transactions:", csv_transactions)

# # Чтение Excel
excel_transactions = read_excel_file(Path("./data/transactions_excel.xlsx"))
print("Excel Transactions:", excel_transactions)