from src.domain.entities import UserEntity
from src.service_layer.entities import (
    AccessToken,
    RefreshToken,
    UserJWTPayload,
    UserPayload,
)
from src.service_layer.services.base import IUserJWTAuthorizationService


def test_create_access_jwt_by_refresh_jwt(
    user_jwt_service_with_user_jwt_refresh: IUserJWTAuthorizationService,
):
    jwt = user_jwt_service_with_user_jwt_refresh.create_access()

    assert jwt
    assert isinstance(jwt, AccessToken)
    assert jwt.access_token


def test_create_refresh_jwt_by_none_jwt(
    created_user: UserEntity,
    user_jwt_service_with_none_jwt: IUserJWTAuthorizationService,
):
    jwt = user_jwt_service_with_none_jwt.create_refresh(created_user)

    assert jwt
    assert isinstance(jwt, RefreshToken)
    assert jwt.refresh_token


def test_get_current_payload_from_access_jwt(
    created_user_jwt_payload: UserPayload,
    user_jwt_service_with_user_jwt_access: IUserJWTAuthorizationService,
):
    user_jwt_payload = user_jwt_service_with_user_jwt_access.current_payload

    assert user_jwt_payload
    assert isinstance(user_jwt_payload, UserJWTPayload)

    assert user_jwt_payload.username == created_user_jwt_payload.username
    assert user_jwt_payload.sub == created_user_jwt_payload.sub
