import pytest
from flask import url_for
from flask.testing import FlaskClient

from api.extension import bearer
from api.models import User
from api.routes.auth.refresh import refresh_endpoint
from api.utils.jwt import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    create_access_jwt,
    create_refresh_jwt,
    decode_jwt,
    response_invalid_token_type_401,
)
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.token import AccessTokenInfo
from common.pydantic_schemas.user import UserValidate


@pytest.mark.auth
@pytest.mark.refresh
class TestRefreshAccessToken:

    def test_refresh_200(
        self,
        client: FlaskClient,
        exist_db_user: User,
    ):
        user = UserValidate.model_validate(exist_db_user)
        access_token = f"{bearer} {create_refresh_jwt(user)}"
        headers = {"Authorization": access_token}
        response = client.post(
            url_for(refresh_endpoint),
            headers=headers,
        )
        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(AccessTokenInfo)
        token_info = AccessTokenInfo.model_validate(response.response_json)
        assert bearer == token_info.token_type
        decoded_access = decode_jwt(token_info.access_token)
        assert exist_db_user.id == decoded_access["sub"]
        assert exist_db_user.username == decoded_access["username"]
        assert ACCESS_TOKEN_TYPE == decoded_access[TOKEN_TYPE_FIELD]

    def test_refresh_invalid_token_type_401(
        self,
        client: FlaskClient,
        exist_db_user: User,
    ):
        user = UserValidate.model_validate(exist_db_user)
        refresh_token = f"{bearer} {create_access_jwt(user)}"
        headers = {"Authorization": refresh_token}
        response = client.post(
            url_for(refresh_endpoint),
            headers=headers,
        )
        expectation = {
            "message": response_invalid_token_type_401.format(
                ACCESS_TOKEN_TYPE.__repr__(),
                REFRESH_TOKEN_TYPE.__repr__(),
            )
        }
        response = Response(response)
        response.assert_status_code(HTTP.UNAUTHORIZED_401)
        response.assert_data(expectation)
