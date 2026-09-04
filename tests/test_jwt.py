from app.core.jwt import create_access_token, verify_access_token


def test_create_and_verify_token():
    data = {
        "sub": "test@example.com"
    }

    token = create_access_token(data)

    payload = verify_access_token(token)

    assert payload is not None
    assert payload["sub"] == "test@example.com"


def test_invalid_token_fails():
    token = "this-is-not-a-valid-token"

    payload = verify_access_token(token)

    assert payload is None