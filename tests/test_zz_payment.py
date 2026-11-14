"""Intentionally alphabetically last and quick: good for demonstrating QTF."""

from decimal import Decimal
from shop.payment import discounted_total, shipping_fee, grand_total


def test_discounted_total():
    # The controlled regression affects this test when DEMO_BUG=1.
    assert discounted_total(Decimal("100.00"), 20) == Decimal("80.00")


def test_free_shipping():
    assert shipping_fee(Decimal("75.00")) == Decimal("0.00")


def test_standard_shipping():
    assert shipping_fee(Decimal("20.00")) == Decimal("4.95")


def test_grand_total():
    assert grand_total(Decimal("80.00"), Decimal("4.95")) == Decimal("84.95")
