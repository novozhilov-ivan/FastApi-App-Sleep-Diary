from datetime import datetime, UTC

import pytest

from src.domain.identity.entities import AccessTokenClaims
from src.domain.identity.exceptions import JWTExpiredError
from src.domain.identity.types import TokenType


def test_create_access_claims_timestamp_seconds_now() -> None:
    now = int(datetime.now(UTC).timestamp())
    before = now - 1
    after = now + 1

    assert before < AccessTokenClaims.timestamp_seconds_now() < after


def test_create_access_claims(subject: str, username: str) -> None:
    assert AccessTokenClaims(
        subject=subject,
        expired_at=int(datetime.now(UTC).timestamp()),
        token_type=TokenType.ACCESS,
        username=username,
    )


def test_access_token_claims_as_dict(
    subject: str,
    issued_at: int,
    expired_at: int,
    jwt_token_ident: str,
    username: str,
) -> None:
    result_dict = {
        "sub": subject,
        "iat": issued_at,
        "exp": expired_at,
        "jti": jwt_token_ident,
        "typ": TokenType.ACCESS,
        "username": username,
    }
    claims = AccessTokenClaims(
        subject=subject,
        issued_at=issued_at,
        expired_at=expired_at,
        jwt_token_ident=jwt_token_ident,
        token_type=TokenType.ACCESS,
        username=username,
    )
    assert result_dict == claims.as_dict()


def test_access_token_claims_validate(
    subject: str,
    issued_at: int,
    jwt_token_ident: str,
    username: str,
) -> None:
    expired_at = 0

    with pytest.raises(JWTExpiredError):
        AccessTokenClaims(
            subject=subject,
            issued_at=issued_at,
            expired_at=expired_at,
            jwt_token_ident=jwt_token_ident,
            token_type=TokenType.ACCESS,
            username=username,
        )
