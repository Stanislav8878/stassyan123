import pytest
from unittest.mock import mock_open, patch, MagicMock
from pathlib import Path

from src.file_handlers import read_csv_file, read_excel_file

# Тесты для CSV файлов
def test_read_csv_file_valid():
    """Тест чтения корректного CSV файла"""
    csv_data = "id,amount,currency\n1,100,USD\n2,200,EUR"
    with patch("builtins.open", mock_open(read_data=csv_data)):
        result = read_csv_file(Path("test.csv"))
        assert result == [
            {"id": "1", "amount": "100", "currency": "USD"},
            {"id": "2", "amount": "200", "currency": "EUR"}
        ]


def test_read_csv_file_empty():
    """Тест чтения пустого CSV файла"""
    with patch("builtins.open", mock_open(read_data="")):
        result = read_csv_file("empty.csv")
        assert result == []


def test_read_csv_file_not_found():
    """Тест обработки отсутствующего файла"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_csv_file("missing.csv")
        assert result == []


# Тесты для Excel файлов
@patch("openpyxl.load_workbook")
def test_read_excel_file_valid(mock_load):
    """Тест чтения корректного Excel файла"""
    # Настраиваем моки
    mock_workbook = MagicMock()
    mock_sheet = MagicMock()
    mock_load.return_value = mock_workbook
    mock_workbook.active = mock_sheet

    # Мокируем заголовки
    header_cells = [
        MagicMock(value="id"),
        MagicMock(value="amount"),
        MagicMock(value="currency")
    ]
    mock_sheet.__getitem__.return_value = header_cells

    # Мокируем данные
    mock_sheet.iter_rows.return_value = [
        (1, 100, "USD"),
        (2, 200, "EUR")
    ]

    result = read_excel_file(Path("test.xlsx"))
    assert result == [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "EUR"}
    ]


@patch("openpyxl.load_workbook", side_effect=FileNotFoundError)
def test_read_excel_file_not_found(mock_load):
    """Тест обработки отсутствующего Excel файла"""
    result = read_excel_file("missing.xlsx")
    assert result == []