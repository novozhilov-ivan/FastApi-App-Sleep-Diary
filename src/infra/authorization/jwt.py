from dataclasses import dataclass
from datetime import timedelta
from typing_extensions import Self

from src.domain.entities.user import UserEntity
from src.infra.authorization.base import BaseTokenService, JWTTypes


@dataclass
class JWTService(BaseTokenService):
    def create_access(self: Self, user: UserEntity) -> dict:
        jwt_payload = {
            "sub": user.oid,
            "username": user.username,
        }

        return {
            "access_token": self._create(
                token_type=JWTTypes.ACCESS,
                token_data=jwt_payload,
            ),
        }

    def create_refresh(self: Self, user: UserEntity) -> dict:
        payload = {
            "sub": user.oid,
            "username": user.username,
        }
        expire_timedelta = timedelta(days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS)

        return {
            "refresh_token": self._create(
                token_type=JWTTypes.REFRESH,
                token_data=payload,
                expire_timedelta=expire_timedelta,
            ),
        }

    def get_token_payload(self: Self, credentials: str) -> dict:
        return self._decode(credentials)

    # def validate_authentication_token():
    #     auth_header: str | None = request.headers.get("Authorization")
    #
    #     if auth_header is None or bearer not in auth_header:
    #         abort(
    #             code=HTTP.UNAUTHORIZED_401,
    #             message=response_invalid_authorization_token_401,
    #         )
    #     *_, token = auth_header.split(" ")
    #     decode_jwt(token=token)
    #
    #     return decorated

    # def get_current_token_payload(
    #     self: Self,
    #     credentials=Headers("Authorization"),
    # ) -> dict:
    #     *_, token = credentials.split(" ")
    #     return self.decode_jwt(token=token)
    #
    # @staticmethod
    # def get_user_oid_by_token_sub(payload: dict) -> UUID:
    #     return payload.get("sub")
    #
    # def get_auth_user_from_token_of_type(
    #     self: Self,
    #     token_type: JWTTypes,
    # ) -> Callable:
    #     def get_current_auth_user_id() -> int:
    #         payload: dict = get_current_token_payload()
    #         validate_token_type(payload, token_type)
    #         current_user = get_user_id_by_token_sub(payload)
    #         return current_user
    #
    #     return get_current_auth_user_id
    #
    # get_current_auth_user_id_for_refresh = get_auth_user_from_token_of_type(
    #     token_type=JWTTypes.REFRESH,
    # )
    # get_current_auth_user_id_for_access = get_auth_user_from_token_of_type(
    #     token_type=JWTTypes.ACCESS,
    # )


# class UserActions:
#     @property
#     def current_user_id(self) -> int:
#         return get_current_auth_user_id_for_access()
