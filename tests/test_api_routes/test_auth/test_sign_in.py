import pytest
from flask import url_for
from flask.testing import FlaskClient

from api.extension import bearer
from api.models import User
from api.routes.auth.sign_in import signin_endpoint
from api.utils.auth import response_invalid_username_or_password_401
from api.utils.jwt import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    decode_jwt,
)
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.token import TokenInfo
from common.pydantic_schemas.user import UserCredentials


@pytest.mark.auth
@pytest.mark.sign_in
class TestSignIn:
    content_type = "application/x-www-form-urlencoded"

    def test_sign_in_200(
        self,
        client: FlaskClient,
        exist_db_user: User,
        user_credentials: UserCredentials,
    ):
        user = UserCredentials.model_validate(user_credentials)
        response = client.post(
            url_for(signin_endpoint),
            data=user.model_dump(),
            content_type=self.content_type,
        )
        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(TokenInfo)
        token_info = TokenInfo.model_validate(response.response_json)
        assert bearer == token_info.token_type
        decoded_access = decode_jwt(token_info.access_token)
        decoded_refresh = decode_jwt(token_info.refresh_token)
        assert exist_db_user.id == decoded_access["sub"] == decoded_refresh["sub"]
        assert exist_db_user.login == decoded_access["username"]
        assert exist_db_user.login == decoded_refresh["username"]
        assert ACCESS_TOKEN_TYPE == decoded_access[TOKEN_TYPE_FIELD]
        assert REFRESH_TOKEN_TYPE == decoded_refresh[TOKEN_TYPE_FIELD]

    @pytest.mark.parametrize(
        "wrong_credentials",
        (
            {"password": "wrong".encode()},
            {"username": "wrong"},
        ),
    )
    def test_sign_in_401(
        self,
        wrong_credentials: dict,
        client: FlaskClient,
        user_credentials: UserCredentials,
        exist_db_user: User,
    ):
        user_credentials = user_credentials.model_dump()
        user_credentials.update(wrong_credentials)
        expectation = {
            "message": response_invalid_username_or_password_401,
        }
        response = client.post(
            url_for(signin_endpoint),
            data=user_credentials,
            content_type=self.content_type,
        )
        response = Response(response)
        response.assert_status_code(HTTP.UNAUTHORIZED_401)
        response.assert_data(expectation)
