from datetime import timedelta
from uuid import UUID

import pytest

from src.infra.jwt import IJWTService, JWTPayload, JWTType
from src.project.settings import AuthJWTSettings


def test_encode_payload(jwt_service: IJWTService):
    payload = {"hello": "world"}
    jwt = jwt_service._encode(payload)
    assert jwt
    assert isinstance(jwt, str)
    assert payload == jwt_service._decode(jwt)


def test_decode_jwt(
    created_access_jwt: str,
    jwt_service: IJWTService,
    jwt_external_payload: dict,
):
    jwt_payload = jwt_service._decode(created_access_jwt)
    assert jwt_payload
    assert jwt_external_payload.items() <= jwt_payload.items()
    assert isinstance(jwt_payload, dict)


@pytest.mark.parametrize(
    ("jwt_type", "expire_seconds"),
    [
        (
            JWTType.ACCESS,
            timedelta(
                minutes=AuthJWTSettings().ACCESS_TOKEN_EXPIRE_MINUTES,
            ).total_seconds(),
        ),
        (
            JWTType.REFRESH,
            timedelta(
                days=AuthJWTSettings().REFRESH_TOKEN_EXPIRE_DAYS,
            ).total_seconds(),
        ),
    ],
)
def test_create_access_jwt(
    jwt_service: IJWTService,
    jwt_type: JWTType,
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
    assert round(jwt_payload.exp - jwt_payload.iat) == expire_seconds


def test_get_jwt_payload(
    jwt_service: IJWTService,
    created_access_jwt: str,
    jwt_external_payload: dict,
):
    jwt_payload = jwt_service.get_jwt_payload(created_access_jwt)

    assert jwt_payload
    assert isinstance(jwt_payload, dict)
    assert jwt_external_payload.items() <= jwt_payload.items()
