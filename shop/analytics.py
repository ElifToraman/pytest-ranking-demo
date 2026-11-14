"""Tiny analytics functions used by deliberately slow tests."""


def average(values: list[int]) -> float:
    if not values:
        raise ValueError("need at least one value")
    return sum(values) / len(values)


def maximum(values: list[int]) -> int:
    return max(values)


def min_max_spread(values: list[int]) -> int:
    return max(values) - min(values)
