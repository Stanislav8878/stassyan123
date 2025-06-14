# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, List

import openpyxl


def read_csv_file(file_path: Path | str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из CSV-файла и возвращает список словарей.

    Args:
        file_path: Путь к CSV-файлу.

    Returns:
        Список словарей с транзакциями. Каждая транзакция представлена в виде словаря.
    """
    transactions = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=",")
            transactions = [row for row in reader]
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Ошибка при чтении CSV-файла: {e}")
    return transactions


def read_excel_file(file_path: Path | str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из Excel-файла и возвращает список словарей.

    Args:
        file_path: Путь к Excel-файлу.

    Returns:
        Список словарей с транзакциями. Каждая транзакция представлена в виде словаря.
    """
    transactions = []
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        headers = [cell.value for cell in sheet[1]]  # Первая строка - заголовки
        for row in sheet.iter_rows(min_row=2, values_only=True):
            transaction = dict(zip(headers, row))
            transactions.append(transaction)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Ошибка при чтении Excel-файла: {e}")
    return transactions
