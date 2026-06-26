from typing import Any, Dict, List
import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected_len",
    [
        ("EXECUTED", 2),
        ("CANCELED", 1),
        ("PENDING", 1),
        ("NON_EXISTENT", 0),
    ],
)
def test_filter_by_state(sample_transactions: List[Dict[str, Any]], state: str, expected_len: int) -> None:
    filtered = filter_by_state(sample_transactions, state)
    assert len(filtered) == expected_len
    for item in filtered:
        assert item["state"] == state


@pytest.mark.parametrize(
    "order_flag, first_id, last_id",
    [
        (True, 2, 3),
        (False, 3, 2),
    ],
)
def test_sort_by_date(sample_transactions: List[Dict[str, Any]], order_flag: bool, first_id: int, last_id: int) -> None:
    sorted_list = sort_by_date(sample_transactions, order_flag)
    assert sorted_list[0]["id"] == first_id
    assert sorted_list[-1]["id"] == last_id
