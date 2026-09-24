import uuid

import jwt

from cv_matcher.core.config import settings
from cv_matcher.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_allows_verification_with_correct_password() -> None:
    hashed = hash_password("supersecret123")

    assert verify_password("supersecret123", hashed) is True


def test_verify_password_rejects_wrong_password() -> None:
    hashed = hash_password("supersecret123")

    assert verify_password("wrong-password", hashed) is False


def test_decode_access_token_roundtrips_subject() -> None:
    user_id = uuid.uuid4()
    token = create_access_token(subject=user_id)

    assert decode_access_token(token) == user_id


def test_decode_access_token_rejects_token_without_subject() -> None:
    token = jwt.encode({}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    assert decode_access_token(token) is None


def test_decode_access_token_rejects_non_uuid_subject() -> None:
    token = jwt.encode(
        {"sub": "not-a-uuid"}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )

    assert decode_access_token(token) is None
