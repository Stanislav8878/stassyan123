import json
import logging
from pathlib import Path
from typing import Any, Dict, List, TypedDict, Union

# Настройка логгера для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Очистка предыдущих handlers (если есть)
logger.handlers = []

# Создаем file handler для записи в файл
file_handler = logging.FileHandler("logs/utils.log", mode="w")
file_handler.setLevel(logging.DEBUG)

# Создаем форматтер
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

# Добавляем handler к логгеру
logger.addHandler(file_handler)


class Transaction(TypedDict, total=False):
    id: int
    state: str
    date: str
    operationAmount: Dict[str, Any]
    description: str
    from_: str
    to: str


def read_json_file(file_path: Union[str, Path]) -> List[Transaction]:
    """
    Читает JSON-файл и возвращает список транзакций.
    Логирует успешные и ошибочные операции.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Успешно прочитан файл: {file_path}")
            return data if isinstance(data, list) else []
    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {file_path}. Ошибка: {str(e)}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}. Ошибка: {str(e)}")
        return []
    except PermissionError as e:
        logger.error(f"Ошибка доступа к файлу {file_path}. Ошибка: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении файла {file_path}. Ошибка: {str(e)}")
        return []
