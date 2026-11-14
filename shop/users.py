"""Simple account validation functions."""


def normalize_email(email: str) -> str:
    return email.strip().lower()


def is_valid_username(username: str) -> bool:
    return username.replace("_", "").isalnum() and 3 <= len(username) <= 20


def can_sign_in(active: bool, suspended: bool) -> bool:
    return active and not suspended
