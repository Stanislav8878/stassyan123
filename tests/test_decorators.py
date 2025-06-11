import os
import pytest
from decorators import log
from datetime import datetime

def test_log_to_console(capsys):
    """Тест логирования в консоль."""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(1, 2)
    captured = capsys.readouterr()
    assert "add ok" in captured.out
    assert result == 3


def test_log_to_file(tmp_path):
    """Тест логирования в файл."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def divide(a: int, b: int) -> float:
        return a / b

    # Тест успешного выполнения
    result = divide(10, 2)
    assert result == 5
    assert "divide ok" in log_file.read_text()

    # Тест ошибки
    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass

    log_content = log_file.read_text()
    assert "divide error: ZeroDivisionError" in log_content
    assert "Inputs: (10, 0), {}" in log_content


def test_log_with_kwargs(capsys):
    """Тест с именованными аргументами."""

    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")
    captured = capsys.readouterr()
    assert "greet ok" in captured.out
    assert result == "Hi, Alice!"


def test_log_preserves_function_metadata():
    """Тест сохранения метаданных функции."""

    @log()
    def sample_func(a: int, b: int) -> int:
        """Sample function for testing."""
        return a + b

    assert sample_func.__name__ == "sample_func"
    assert sample_func.__doc__ == "Sample function for testing."
    assert sample_func.__annotations__ == {"a": int, "b": int, "return": int}


def test_log_with_existing_file(tmp_path):
    """Тест добавления логов в существующий файл."""
    log_file = tmp_path / "existing.log"
    log_file.write_text("Existing content\n")

    @log(filename=str(log_file))
    def test_func() -> None:
        pass

    test_func()

    content = log_file.read_text()
    assert "Existing content" in content
    assert "test_func ok" in content