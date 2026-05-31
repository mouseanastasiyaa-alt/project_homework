import pytest


@pytest.fixture
def card_numbers_raw():
    return {
        "valid_16": "7000792289606361",
        "valid_16_alt": "1234567812345678",
        "empty": "",
    }


@pytest.fixture
def account_numbers_raw():
    return {
        "valid_20": "73654108430135874305",
        "short": "123",
        "empty": "",
    }


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "CANCELED", "date": "2024-03-12T11:45:05.123456"},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-09T18:12:10.000000"},
        {"id": 4, "state": "PENDING", "date": "2024-03-10T00:00:00.000000"},
    ]
