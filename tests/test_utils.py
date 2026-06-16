import json
from unittest.mock import mock_open, patch

from src.utils import get_financial_data


def test_read_json_file_success() -> None:
    """Тест успешного чтения корректного JSON-файла."""
    mock_data = [{"id": 1, "amount": "100.00"}]
    mock_json = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("os.path.exists", return_value=True):
            result = get_financial_data("dummy_path.json")
            assert result == mock_data


def test_read_json_file_not_list() -> None:
    """Тест ситуации, когда JSON содержит словарь вместо списка."""
    mock_data = {"id": 1, "amount": "100.00"}
    mock_json = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("os.path.exists", return_value=True):
            result = get_financial_data("dummy_path.json")
            assert result == []


def test_read_json_file_invalid_or_empty() -> None:
    """Тест ситуации с пустым или поврежденным файлом."""
    with patch("builtins.open", mock_open(read_data="")):
        with patch("os.path.exists", return_value=True):
            result = get_financial_data("dummy_path.json")
            assert result == []


def test_read_json_file_not_found() -> None:
    """Тест ситуации, когда файл не существует."""
    with patch("os.path.exists", return_value=False):
        result = get_financial_data("non_existent_file.json")
        assert result == []
