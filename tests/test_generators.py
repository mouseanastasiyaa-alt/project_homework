from typing import Any, Dict, List
import pytest
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура для depth-генерации тестовых данных транзакций."""
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "operationAmount": {"currency": {"name": "USD", "code": "USD"}},
        },
        {
            "id": 2,
            "description": "Перевод со счета на счет",
            "operationAmount": {"currency": {"name": "RUB", "code": "RUB"}},
        },
        {
            "id": 3,
            "description": "Покупка авиабилетов",
            "operationAmount": {"currency": {"name": "USD", "code": "USD"}},
        },
    ]


@pytest.mark.parametrize(
    "currency, expected_count, expected_ids",
    [
        ("USD", 2, [1, 3]),
        ("RUB", 1, [2]),
        ("EUR", 0, []),
    ],
)
def test_filter_by_currency(
    sample_transactions: List[Dict[str, Any]], currency: str, expected_count: int, expected_ids: List[int]
) -> None:
    """Параметризованный тест для проверки фильтрации валют."""
    result = list(filter_by_currency(sample_transactions, currency))
    assert len(result) == expected_count
    assert [item["id"] for item in result] == expected_ids


def test_transaction_descriptions(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест генератора описаний транзакций."""
    descriptions = list(transaction_descriptions(sample_transactions))
    assert descriptions == ["Перевод организации", "Перевод со счета на счет", "Покупка авиабилетов"]


@pytest.mark.parametrize(
    "start, stop, expected_list",
    [
        (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
        (999, 1000, ["0000 0000 0000 0999", "0000 0000 0000 1000"]),
    ],
)
def test_card_number_generator(start: int, stop: int, expected_list: List[str]) -> None:
    """Параметризованный тест генератора номеров карт."""
    result = list(card_number_generator(start, stop))
    assert result == expected_list
