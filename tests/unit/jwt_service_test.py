from datetime import UTC, datetime, timedelta
from operator import add
from uuid import UUID

import pytest

from src.infra.jwt import IJWTService, JWTPayload, JWTService, JWTType
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
                minutes=AuthJWTSettings().access_token_expire,
            ).total_seconds(),
        ),
        (
            JWTType.REFRESH,
            timedelta(
                days=AuthJWTSettings().refresh_token_expire,
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


@pytest.mark.parametrize(
    ("jwt_type", "expected_expire_seconds", "expire_timedelta"),
    [
        (JWTType.ACCESS, 30, timedelta(seconds=30)),
        (JWTType.REFRESH, 30, timedelta(seconds=30)),
        (JWTType.ACCESS, 60, timedelta(minutes=1)),
        (JWTType.REFRESH, 60, timedelta(minutes=1)),
        (JWTType.ACCESS, 60 * 60, timedelta(hours=1)),
        (JWTType.REFRESH, 60 * 60, timedelta(hours=1)),
        (JWTType.ACCESS, 60 * 60 * 24, timedelta(days=1)),
        (JWTType.REFRESH, 60 * 60 * 24, timedelta(days=1)),
        (
            JWTType.ACCESS,
            timedelta(
                minutes=AuthJWTSettings().access_token_expire,
            ).total_seconds(),
            None,
        ),
        (
            JWTType.REFRESH,
            timedelta(
                days=AuthJWTSettings().refresh_token_expire,
            ).total_seconds(),
            None,
        ),
    ],
)
def test_get_expire_at(
    jwt_type: JWTType,
    expected_expire_seconds: float,
    expire_timedelta: timedelta | None,
    jwt_service: JWTService,
):
    expected_expire_at_seconds = add(
        datetime.now(UTC).timestamp(),
        expected_expire_seconds,
    )

    expire_at_seconds = jwt_service.get_expired_at(jwt_type, expire_timedelta)

    assert expected_expire_at_seconds <= expire_at_seconds

    expected_seconds_difference = 0.01
    seconds_difference = expire_at_seconds - expected_expire_at_seconds
    assert seconds_difference < expected_seconds_difference
