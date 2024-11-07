from datetime import UTC, datetime
from uuid import UUID

import pytest

from src.project.settings import AuthJWTSettings
from src.service_layer.entities import IPayload, JWTPayload, TokenType
from src.service_layer.services.base import IJWTService
from src.service_layer.services.jwt import JWTService


def test_encode_payload(jwt_service: IJWTService):
    payload = {"hello": "world"}
    jwt = jwt_service.encode(payload)
    assert jwt
    assert isinstance(jwt, str)
    assert payload == jwt_service.decode(jwt)


def test_decode_jwt(
    created_user_access_jwt: str,
    jwt_service: IJWTService,
    created_user_jwt_payload: IPayload,
):
    jwt_payload = jwt_service.decode(created_user_access_jwt)
    assert jwt_payload
    assert created_user_jwt_payload.convert_to_dict().items() <= jwt_payload.items()
    assert isinstance(jwt_payload, dict)


@pytest.mark.parametrize(
    ("jwt_type", "expire_seconds"),
    [
        (TokenType.ACCESS, AuthJWTSettings().access_token_expire),
        (TokenType.REFRESH, AuthJWTSettings().refresh_token_expire),
    ],
)
def test_create_access_jwt(
    jwt_service: IJWTService,
    jwt_type: TokenType,
    expire_seconds: float,
):
    jwt = jwt_service.create_jwt(jwt_type)
    assert jwt

    jwt_payload = JWTPayload(**jwt_service.get_jwt_payload(jwt))

    assert jwt_payload
    assert jwt_payload.typ == jwt_type
    assert jwt_payload.iat
    assert jwt_payload.jti
    assert jwt_payload.iat < jwt_payload.exp
    assert UUID(jwt_payload.jti)
    assert jwt_payload.exp - jwt_payload.iat == expire_seconds


def test_get_jwt_payload(
    jwt_service: IJWTService,
    created_user_access_jwt: str,
    created_user_jwt_payload: IPayload,
):
    jwt_payload = jwt_service.get_jwt_payload(created_user_access_jwt)

    assert jwt_payload
    assert isinstance(jwt_payload, dict)
    assert created_user_jwt_payload.convert_to_dict().items() <= jwt_payload.items()


@pytest.mark.parametrize(
    ("jwt_type", "expected_expire"),
    [
        (TokenType.ACCESS, 30),
        (TokenType.REFRESH, 30),
        (TokenType.ACCESS, 60),
        (TokenType.REFRESH, 60),
        (TokenType.ACCESS, 60 * 60),
        (TokenType.REFRESH, 60 * 60),
        (TokenType.ACCESS, 60 * 60 * 24),
        (TokenType.REFRESH, 60 * 60 * 24),
        (TokenType.ACCESS, AuthJWTSettings().access_token_expire),
        (TokenType.REFRESH, AuthJWTSettings().refresh_token_expire),
    ],
)
def test_get_expire_at(
    jwt_type: TokenType,
    expected_expire: int,
    jwt_service: JWTService,
):
    expected_expire_at = int(datetime.now(UTC).timestamp() + expected_expire)

    expire_at = jwt_service.get_expired_at(jwt_type, expected_expire)

    assert expected_expire_at <= expire_at

    expected_seconds_difference = 0
    seconds_difference = expire_at - expected_expire_at
    assert seconds_difference == expected_seconds_difference
