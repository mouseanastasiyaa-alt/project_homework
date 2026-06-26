import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("Visa Gold 7000792289606361", "Visa Gold 7000 79** **** 6361"),
        ("Маэстро 1234567812345678", "Маэстро 1234 56** **** 5678"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(input_data: str, expected: str) -> None:
    assert mask_account_card(input_data) == expected


def test_mask_account_card_empty() -> None:
    res = mask_account_card("")
    assert isinstance(res, str)


@pytest.mark.parametrize(
    "date_input, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2025-12-31T23:59:59.999999", "31.12.2025"),
    ],
)
def test_get_date(date_input: str, expected: str) -> None:
    assert get_date(date_input) == expected
