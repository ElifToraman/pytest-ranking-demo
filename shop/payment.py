"""Payment calculations. DEMO_BUG is an explicit teaching-only fault switch."""

import os
from decimal import Decimal


def discounted_total(amount: Decimal, percent: int) -> Decimal:
    """Return a money amount after an integer percentage discount."""
    if amount < 0:
        raise ValueError("amount must be nonnegative")
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")

    # Deliberately inject a regression for a controlled CI demonstration.
    # Leave DEMO_BUG unset (or '0') for correct production behavior.
    if os.getenv("DEMO_BUG") == "1" and percent >= 20:
        multiplier = Decimal(100 + percent) / Decimal(100)
    else:
        multiplier = Decimal(100 - percent) / Decimal(100)
    return (amount * multiplier).quantize(Decimal("0.01"))


def shipping_fee(subtotal: Decimal) -> Decimal:
    return Decimal("0.00") if subtotal >= Decimal("50.00") else Decimal("4.95")


def grand_total(subtotal: Decimal, shipping: Decimal) -> Decimal:
    return (subtotal + shipping).quantize(Decimal("0.01"))
