import pytest
from flask import url_for
from flask.testing import FlaskClient

from src.extension import bearer
from src.models import UserOrm
from src.pydantic_schemas.token import TokenInfo
from src.pydantic_schemas.user import UserCredentials
from src.routes.auth.sign_in import signin_endpoint
from src.utils.auth import response_invalid_username_or_password_401
from src.utils.jwt import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    decode_jwt,
)
from src.utils.status_codes import HTTP
from tests.api.response import Response


@pytest.mark.auth
@pytest.mark.sign_in
class TestSignIn:
    content_type = "application/x-www-form-urlencoded"

    def test_sign_in_200(
        self,
        client: FlaskClient,
        exist_user: UserOrm,
        user_credentials: UserCredentials,
    ):
        user = UserCredentials.model_validate(user_credentials)
        raw_response = client.post(
            path=url_for(
                endpoint=signin_endpoint,
            ),
            data=user.model_dump(),
            content_type=self.content_type,
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(TokenInfo)
        token_info = TokenInfo.model_validate(response.response_json)
        assert bearer == token_info.token_type
        decoded_access = decode_jwt(token_info.access_token)
        decoded_refresh = decode_jwt(token_info.refresh_token)
        assert exist_user.id == decoded_access["sub"] == decoded_refresh["sub"]
        assert exist_user.username == decoded_access["username"]
        assert exist_user.username == decoded_refresh["username"]
        assert ACCESS_TOKEN_TYPE == decoded_access[TOKEN_TYPE_FIELD]
        assert REFRESH_TOKEN_TYPE == decoded_refresh[TOKEN_TYPE_FIELD]

    @pytest.mark.parametrize(
        "wrong_credentials",
        (
            {"password": "super_wrong_password".encode()},
            {"username": "super_wrong_username"},
        ),
    )
    def test_sign_in_401(
        self,
        wrong_credentials: dict,
        client: FlaskClient,
        user_credentials: UserCredentials,
        exist_user: UserOrm,
    ):
        user_credentials_dump: dict = user_credentials.model_dump()
        user_credentials_dump.update(wrong_credentials)
        raw_response = client.post(
            path=url_for(
                endpoint=signin_endpoint,
            ),
            data=user_credentials_dump,
            content_type=self.content_type,
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.UNAUTHORIZED_401)
        error_expectation = {"message": response_invalid_username_or_password_401}
        response.assert_data(error_expectation)
