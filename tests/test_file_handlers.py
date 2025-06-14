import pytest
from unittest.mock import mock_open, patch
from pathlib import Path

from src.file_handlers import read_csv_file, read_excel_file


def test_read_csv_file_valid():
    csv_data = """id,amount,currency
1,100,USD
2,200,EUR"""
    with patch("builtins.open", mock_open(read_data=csv_data)):
        result = read_csv_file(Path("dummy.csv"))
        assert result == [
            {"id": "1", "amount": "100", "currency": "USD"},
            {"id": "2", "amount": "200", "currency": "EUR"},
        ]


def test_read_csv_file_empty():
    csv_data = ""
    with patch("builtins.open", mock_open(read_data=csv_data)):
        result = read_csv_file(Path("empty.csv"))
        assert result == []


def test_read_csv_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_csv_file(Path("nonexistent.csv"))
        assert result == []


@patch("openpyxl.load_workbook")
def test_read_excel_file_valid(mock_load):
    mock_workbook = mock_load.return_value
    mock_sheet = mock_workbook.active
    mock_sheet.iter_rows.return_value = [
        (1, 100, "USD"),
        (2, 200, "EUR"),
    ]
    mock_sheet[1] = [
        mock_cell("id"),
        mock_cell("amount"),
        mock_cell("currency"),
    ]

    result = read_excel_file(Path("dummy.xlsx"))
    assert result == [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "EUR"},
    ]


def mock_cell(value):
    cell = type("Cell", (), {"value": value})
    return cell


@patch("openpyxl.load_workbook", side_effect=FileNotFoundError)
def test_read_excel_file_not_found(mock_load):
    result = read_excel_file(Path("nonexistent.xlsx"))
    assert result == []