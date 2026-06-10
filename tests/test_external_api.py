from unittest.mock import MagicMock, patch
from src.external_api import convert_currency


def test_convert_currency_rub() -> None:
    """Тест транзакции, которая изначально в рублях."""
    transaction = {
        "operationAmount": {
            "amount": "1500.50",
            "currency": {"name": "руб.", "code": "RUB"}
        }
    }
    result = convert_currency(transaction)
    assert result == 1500.50


@patch("requests.get")
@patch("os.getenv")
def test_convert_currency_usd_success(mock_getenv: MagicMock, mock_get: MagicMock) -> None:
    """Тест успешной конвертации USD в RUB через API."""
    mock_getenv.return_value = "fake_api_key"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 7500.00}
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "USD", "code": "USD"}
        }
    }

    result = convert_currency(transaction)
    assert result == 7500.00


@patch("requests.get")
@patch("os.getenv")
def test_convert_currency_api_error(mock_getenv: MagicMock, mock_get: MagicMock) -> None:
    """Тест ситуации, когда сервер API вернул ошибку."""
    mock_getenv.get.return_value = "fake_api_key"

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "EUR", "code": "EUR"}
        }
    }

    result = convert_currency(transaction)
    assert result == 0.0
