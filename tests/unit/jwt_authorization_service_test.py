from src.domain.entities import UserEntity
from src.service_layer.entities import AccessToken, RefreshToken, UserJWTPayload
from src.service_layer.services.base import IUserJWTAuthorizationService


def test_create_access_jwt(
    created_user: UserEntity,
    jwt_authorization_service: IUserJWTAuthorizationService,
):
    jwt = jwt_authorization_service.create_access(created_user)

    assert jwt
    assert isinstance(jwt, AccessToken)
    assert jwt.access_token


def test_create_refresh_jwt(
    created_user: UserEntity,
    jwt_authorization_service: IUserJWTAuthorizationService,
):
    jwt = jwt_authorization_service.create_refresh(created_user)

    assert jwt
    assert isinstance(jwt, RefreshToken)
    assert jwt.refresh_token


def test_get_payload(
    created_user: UserEntity,
    jwt_authorization_service: IUserJWTAuthorizationService,
):
    jwt = jwt_authorization_service.create_access(created_user)
    user_jwt_payload = jwt_authorization_service.get_payload(jwt.access_token)

    assert user_jwt_payload
    assert isinstance(user_jwt_payload, UserJWTPayload)

    assert user_jwt_payload.username == created_user.username
    assert user_jwt_payload.sub == str(created_user.oid)
