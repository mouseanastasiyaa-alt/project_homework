"""
Тесты для модуля file_reader.
"""

from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.file_reader import read_transactions_from_csv, read_transactions_from_excel


MOCK_TRANSACTIONS = [
    {"id": 1, "amount": 100.50, "description": "Payment 1"},
    {"id": 2, "amount": 200.75, "description": "Payment 2"},
]


class TestReadTransactionsFromCSV:
    """Тесты для функции read_transactions_from_csv."""

    @patch("src.file_reader.os.path.exists")
    @patch("src.file_reader.pd.read_csv")
    def test_successful_read(self, mock_read_csv, mock_exists):
        """Тест успешного чтения CSV файла."""
        mock_exists.return_value = True
        mock_df = Mock()
        mock_df.empty = False
        mock_df.to_dict.return_value = MOCK_TRANSACTIONS
        mock_read_csv.return_value = mock_df

        result = read_transactions_from_csv("test.csv")
        assert result == MOCK_TRANSACTIONS
        mock_read_csv.assert_called_once_with("test.csv")
    @patch("src.file_reader.os.path.exists")
    @patch("src.file_reader.pd.read_csv")
    def test_empty_csv(self, mock_read_csv, mock_exists):
        """Тест чтения пустого CSV файла."""
        mock_exists.return_value = True
        mock_df = Mock()
        mock_df.empty = True
        mock_read_csv.return_value = mock_df

        with pytest.raises(ValueError, match="CSV файл пуст"):
            read_transactions_from_csv("empty.csv")

    @patch("src.file_reader.os.path.exists")
    @patch("src.file_reader.pd.read_csv")
    def test_file_not_found(self, mock_read_csv, mock_exists):
        """Тест обработки отсутствующего файла."""
        mock_exists.return_value = False

        with pytest.raises(FileNotFoundError):
            read_transactions_from_csv("nonexistent.csv")
        mock_read_csv.assert_not_called()


class TestReadTransactionsFromExcel:
    """Тесты для функции read_transactions_from_excel."""

    @patch("src.file_reader.os.path.exists")
    @patch("src.file_reader.pd.read_excel")
    def test_successful_read(self, mock_read_excel, mock_exists):
        """Тест успешного чтения Excel файла."""
        mock_exists.return_value = True
        mock_df = Mock()
        mock_df.empty = False
        mock_df.to_dict.return_value = MOCK_TRANSACTIONS
        mock_read_excel.return_value = mock_df

        result = read_transactions_from_excel("test.xlsx")
        assert result == MOCK_TRANSACTIONS
        mock_read_excel.assert_called_once_with("test.xlsx")

    @patch("src.file_reader.os.path.exists")
    @patch("src.file_reader.pd.read_excel")
    def test_empty_excel(self, mock_read_excel, mock_exists):
        """Тест чтения пустого Excel файла."""
        mock_exists.return_value = True
        mock_df = Mock()
        mock_df.empty = True
        mock_read_excel.return_value = mock_df

        with pytest.raises(ValueError, match="Excel файл пуст"):
            read_transactions_from_excel("empty.xlsx")

    @patch("src.file_reader.os.path.exists")
    @patch("src.file_reader.pd.read_excel")
    def test_file_not_found(self, mock_read_excel, mock_exists):
        """Тест обработки отсутствующего файла."""
        mock_exists.return_value = False

        with pytest.raises(FileNotFoundError):
            read_transactions_from_excel("nonexistent.xlsx")
        mock_read_excel.assert_not_called()
