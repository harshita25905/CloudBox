from app.core.security import hash_password, verify_password


def test_password_hashing():
    password = "mysecretpassword"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)


def test_wrong_password_fails():
    password = "mysecretpassword"

    hashed_password = hash_password(password)

    assert not verify_password("wrongpassword", hashed_password)