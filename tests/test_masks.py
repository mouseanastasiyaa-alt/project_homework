import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize(
    "card_key, expected",
    [
        ("valid_16", "7000 79** **** 6361"),
        ("valid_16_alt", "1234 56** **** 5678"),
        ("empty", " ** **** "),
    ],
)
def test_get_mask_card_number(card_numbers_raw, card_key, expected):
    raw_number = card_numbers_raw[card_key]
    assert get_mask_card_number(raw_number) == expected


@pytest.mark.parametrize(
    "acc_key, expected",
    [
        ("valid_20", "**4305"),
        ("short", "**123"),
        ("empty", "**"),
    ],
)
def test_get_mask_account(account_numbers_raw, acc_key, expected):
    raw_account = account_numbers_raw[acc_key]
    assert get_mask_account(raw_account) == expected
