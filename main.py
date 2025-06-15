from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any, Optional

from file_handlers import read_csv_file, read_excel_file, read_json_file
from masks import get_mask_account, get_mask_card_number
from processing import (
    filter_by_state,
    sort_by_date,
    search_by_description,
    count_transactions_by_category,
)
from widget import get_date, mask_account_card


def print_transaction(transaction: Dict[str, Any]) -> None:
    """Печатает информацию о транзакции в читаемом формате."""
    if not isinstance(transaction, dict):
        return

    date = get_date(transaction.get("date", ""))
    description = transaction.get("description", "Без описания")

    from_ = transaction.get("from", "")
    to = transaction.get("to", "")

    amount_info = transaction.get("operationAmount", {})
    amount = amount_info.get("amount", "0")
    currency_info = amount_info.get("currency", {})
    currency_code = currency_info.get("code", "RUB")

    # Маскировка номеров карт и счетов
    from_masked = mask_account_card(from_) if from_ else ""
    to_masked = mask_account_card(to) if to else ""

    print(f"{date} {description}")
    if from_masked and to_masked:
        print(f"{from_masked} -> {to_masked}")
    elif from_masked:
        print(f"{from_masked}")
    elif to_masked:
        print(f"{to_masked}")

    print(f"Сумма: {amount} {currency_code}\n")


def get_user_choice(prompt: str, valid_choices: List[str]) -> str:
    """Получает выбор пользователя с валидацией."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print(f"Неверный выбор. Допустимые варианты: {', '.join(valid_choices)}")


def main() -> None:
    """Основная функция программы для работы с банковскими транзакциями."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_type = get_user_choice("Ваш выбор (1-3): ", ["1", "2", "3"])

    file_path = Path("./data/transactions")
    if file_type == "1":
        file_path = file_path.with_suffix(".json")
        print("Для обработки выбран JSON-файл.")
    elif file_type == "2":
        file_path = file_path.with_suffix(".csv")
        print("Для обработки выбран CSV-файл.")
    else:
        file_path = file_path.with_suffix(".xlsx")
        print("Для обработки выбран XLSX-файл.")

    # Чтение файла
    if file_type == "1":
        transactions = read_json_file(file_path)
    elif file_type == "2":
        transactions = read_csv_file(file_path)
    else:
        transactions = read_excel_file(file_path)

    if not transactions:
        print("Не удалось загрузить транзакции или файл пуст.")
        return

    # Фильтрация по статусу
    print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING")

    while True:
        state = input("Ваш выбор: ").strip().upper()
        if state in {"EXECUTED", "CANCELED", "PENDING"}:
            break
        print(f'Статус операции "{state}" недоступен.')

    filtered = filter_by_state(transactions, state)
    print(f'Операции отфильтрованы по статусу "{state}"')

    if not filtered:
        print("Не найдено ни одной транзакции с выбранным статусом.")
        return

    # Сортировка по дате
    sort_choice = get_user_choice("\nОтсортировать операции по дате? (да/нет): ", ["да", "нет"])

    if sort_choice == "да":
        order_choice = get_user_choice("Отсортировать по возрастанию или по убыванию? (возрастанию/убыванию): ",
                                       ["возрастанию", "убыванию"])
        reverse = order_choice == "убыванию"
        filtered = sort_by_date(filtered, reverse=reverse)
        print(f"Операции отсортированы по дате ({order_choice})")

    # Фильтрация по рублям
    rub_only = get_user_choice("\nВыводить только рублевые транзакции? (да/нет): ", ["да", "нет"])

    if rub_only == "да":
        filtered = [t for t in filtered
                    if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"]
        print("Оставлены только рублевые транзакции")

    # Поиск по описанию
    search_choice = get_user_choice("\nОтфильтровать список транзакций по определенному слову в описании? (да/нет): ",
                                    ["да", "нет"])

    if search_choice == "да":
        search_string = input("Введите строку для поиска в описании: ").strip()
        if search_string:
            filtered = search_by_description(filtered, search_string)
            print(f'Найдено транзакций по запросу "{search_string}": {len(filtered)}')

    # Подсчет категорий
    categories = count_transactions_by_category(filtered)
    print("\nСтатистика по категориям операций:")
    for category, count in categories.items():
        print(f"{category}: {count} операций")

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(filtered)}\n")

    for transaction in filtered:
        print_transaction(transaction)


if __name__ == "__main__":
    main()