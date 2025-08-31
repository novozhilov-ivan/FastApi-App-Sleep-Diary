from dataclasses import replace

import pytest

from src.domain.identity.entities import AccessTokenClaims
from src.domain.identity.exceptions import (
    AccessTokenIsExpiredError,
    UnauthorizedError,
)
from src.domain.identity.jwt_processor import IJWTProcessor
from src.domain.identity.types import JWTToken
from src.infra.identity.services.access_token_processor import AccessTokenProcessor


def test_access_token_processor_encode(
    access_token_processor: AccessTokenProcessor,
    claims: AccessTokenClaims,
    jwt_token: JWTToken,
) -> None:
    access_token = access_token_processor.encode(claims)

    assert access_token == jwt_token


def test_access_token_processor_decode_correct(
    access_token_processor: AccessTokenProcessor,
    claims: AccessTokenClaims,
    jwt_token: JWTToken,
) -> None:
    decoded_access_token_claims = access_token_processor.decode(jwt_token)

    assert decoded_access_token_claims.as_dict() == claims.as_dict()


def test_access_token_processor_decode_invalid_type(
    access_token_processor: AccessTokenProcessor,
    claims: AccessTokenClaims,
) -> None:
    changed_token_claims = replace(
        claims,
        token_type="some_other_type",  # type: ignore[arg-type]
    )
    token = access_token_processor.encode(changed_token_claims)

    with pytest.raises(UnauthorizedError):
        access_token_processor.decode(token)


@pytest.mark.parametrize(
    "payload_field_key",
    ["sub", "iat", "exp", "jti", "typ", "username"],
)
def test_access_token_processor_decode_token_with_missed_payload_keys(
    access_token_processor: AccessTokenProcessor,
    jwt_processor: IJWTProcessor,
    claims: AccessTokenClaims,
    payload_field_key: str,
) -> None:
    payload = claims.as_dict()
    payload.pop(payload_field_key)
    token = jwt_processor.encode(payload)

    with pytest.raises(UnauthorizedError):
        access_token_processor.decode(token)


def test_access_token_processor_decode_expired_token(
    access_token_processor: AccessTokenProcessor,
    expired_jwt_token: JWTToken,
) -> None:
    with pytest.raises(AccessTokenIsExpiredError):
        access_token_processor.decode(expired_jwt_token)
