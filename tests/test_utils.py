"""
Тесты для модуля utils.
"""

import json
import os
from unittest.mock import mock_open, patch

import pytest

from src.utils import load_transactions_from_json


def test_load_transactions_from_json_success():
    """Тест успешной загрузки JSON файла."""
    mock_data = '[{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]'

    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("os.path.exists", return_value=True):
            result = load_transactions_from_json("test.json")
            assert len(result) == 2
            assert result[0]["id"] == 1


def test_load_transactions_from_json_file_not_found():
    """Тест обработки отсутствующего файла."""
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_transactions_from_json("nonexistent.json")


def test_load_transactions_from_json_invalid_json():
    """Тест обработки некорректного JSON."""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch("os.path.exists", return_value=True):
            with pytest.raises(json.JSONDecodeError):
                load_transactions_from_json("invalid.json")