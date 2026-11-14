"""Slow-ish tests simulate long-running external integrations."""

import time
import pytest
from shop.analytics import average, maximum, min_max_spread


def test_average_values():
    time.sleep(0.40)
    assert average([1, 2, 3, 4]) == 2.5


def test_maximum_value():
    time.sleep(0.35)
    assert maximum([1, 8, 3]) == 8


def test_spread_values():
    time.sleep(0.40)
    assert min_max_spread([2, 6, 10]) == 8


def test_average_empty_input():
    time.sleep(0.35)
    with pytest.raises(ValueError):
        average([])
