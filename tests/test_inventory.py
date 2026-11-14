import time
import pytest
from shop.inventory import can_fulfill, remaining_stock, restock


def test_fulfill_existing_stock():
    time.sleep(0.45)
    assert can_fulfill(10, 5)


def test_reject_insufficient_stock():
    time.sleep(0.35)
    assert not can_fulfill(2, 3)


def test_restock_items():
    time.sleep(0.40)
    assert restock(2, 4) == 6


def test_reject_invalid_remaining_stock():
    time.sleep(0.35)
    with pytest.raises(ValueError):
        remaining_stock(1, 4)
