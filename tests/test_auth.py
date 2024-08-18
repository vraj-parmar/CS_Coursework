import hashlib
from stock_forecasting import (make_hashes, check_hashes)

def test_make_hashes():
    password = "testpassword"
    hashed_password = make_hashes(password)
    assert hashed_password == hashlib.sha256(password.encode()).hexdigest()

def test_check_hashes():
    password = "testpassword"
    hashed_password = make_hashes(password)
    assert check_hashes(password, hashed_password) == hashed_password
    assert check_hashes("wrongpassword", hashed_password) is False
