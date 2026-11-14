import time
from shop.users import normalize_email, is_valid_username, can_sign_in


def test_email_normalization():
    time.sleep(0.40)
    assert normalize_email(" Test@Example.COM ") == "test@example.com"


def test_valid_username():
    time.sleep(0.35)
    assert is_valid_username("guest_42")


def test_invalid_username():
    time.sleep(0.40)
    assert not is_valid_username("a!")


def test_suspended_account_cannot_sign_in():
    time.sleep(0.35)
    assert not can_sign_in(True, True)
