"""Simple stock manipulation functions."""


def can_fulfill(stock: int, requested: int) -> bool:
    return stock >= 0 and requested >= 0 and requested <= stock


def remaining_stock(stock: int, requested: int) -> int:
    if not can_fulfill(stock, requested):
        raise ValueError("insufficient or invalid stock")
    return stock - requested


def restock(stock: int, incoming: int) -> int:
    if stock < 0 or incoming < 0:
        raise ValueError("stock cannot be negative")
    return stock + incoming
