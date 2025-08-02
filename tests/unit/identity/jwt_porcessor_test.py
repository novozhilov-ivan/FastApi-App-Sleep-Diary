import pytest

from src.domain.identity.exceptions import JWTDecodeError, JWTExpiredError
from src.domain.identity.jwt_processor import IJWTProcessor
from src.domain.identity.types import JWTClaims, JWTToken


def test_jwt_processor_encode_payload(
    jwt_processor: IJWTProcessor,
    claims_payload: JWTClaims,
) -> None:
    token = jwt_processor.encode(claims_payload)

    assert token
    assert isinstance(token, str)
    assert isinstance(token, JWTToken)


def test_jwt_processor_decode_token(
    jwt_processor: IJWTProcessor,
    jwt_token: JWTToken,
    claims_payload: JWTClaims,
) -> None:
    decoded_claims_payload = jwt_processor.decode(jwt_token)

    assert decoded_claims_payload == claims_payload
    assert isinstance(decoded_claims_payload, dict)


def test_jwt_processor_decode_expired_token(
    jwt_processor: IJWTProcessor,
    expired_jwt_token: JWTToken,
) -> None:
    with pytest.raises(JWTExpiredError):
        jwt_processor.decode(expired_jwt_token)


def test_jwt_processor_decode_invalid_token(jwt_processor: IJWTProcessor) -> None:
    with pytest.raises(JWTDecodeError):
        jwt_processor.decode("some.trash.values")
