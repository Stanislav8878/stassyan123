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
        file_path: Путь к CSV-файлу (строка или Path объект)

    Returns:
        Список словарей, где каждый словарь представляет одну транзакцию
    """
    transactions = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            transactions = [dict(row) for row in reader]
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {str(e)}")
    return transactions


def read_excel_file(file_path: Path | str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из Excel-файла и возвращает список словарей.

    Args:
        file_path: Путь к Excel-файлу (строка или Path объект)

    Returns:
        Список словарей, где каждый словарь представляет одну транзакцию
    """
    transactions = []
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        # Получаем заголовки из первой строки
        headers = [cell.value for cell in sheet[1]]

        # Читаем данные со второй строки
        for row in sheet.iter_rows(min_row=2, values_only=True):
            transaction = dict(zip(headers, row))
            transactions.append(transaction)

    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {str(e)}")
    return transactions
