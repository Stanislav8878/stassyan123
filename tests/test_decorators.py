import os
import tempfile
import pytest
import logging
from decorators import log


def test_log_success_to_console(capsys):
    """Тест успешного логирования в консоль"""
    # Очищаем все существующие обработчики логов
    logger = logging.getLogger(__name__)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(2, 3)
    assert result == 5

    captured = capsys.readouterr()
    assert "INFO" in captured.out
    assert "add" in captured.out
    assert "Args: (2, 3)" in captured.out
    assert "Result: 5" in captured.out


def test_log_error_to_file():
    """Тест логирования ошибок в файл"""
    # Создаем временный файл с автоматическим удалением
    with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tmp:
        @log(filename=tmp.name)
        def fail_func():
            raise ValueError("Test error message")

        # Проверяем что исключение пробрасывается
        with pytest.raises(ValueError):
            fail_func()

        # Читаем содержимое файла
        tmp.seek(0)
        content = tmp.read()

        assert "ERROR" in content
        assert "fail_func" in content
        assert "ValueError" in content
        assert "Test error message" in content


def test_log_disabled_levels(capsys):
    """Тест отключения уровней логирования"""

    @log(log_errors=False, log_success=False)
    def silent_func():
        return 42

    result = silent_func()
    assert result == 42

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""