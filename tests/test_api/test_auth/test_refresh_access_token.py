import pytest
from flask import url_for
from flask.testing import FlaskClient
from werkzeug.datastructures import Authorization

from api.extension import bearer
from api.models import UserOrm
from api.routes.auth.refresh import refresh_endpoint
from api.utils.jwt import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    decode_jwt,
    response_invalid_token_type_401,
)
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.token import AccessTokenInfo


@pytest.mark.auth
@pytest.mark.refresh
class TestRefreshAccessToken:

    def test_refresh_200(
        self,
        client: FlaskClient,
        jwt_refresh: Authorization,
        exist_user: UserOrm,
    ):
        response = client.post(
            path=url_for(
                endpoint=refresh_endpoint,
            ),
            auth=jwt_refresh,
        )
        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(AccessTokenInfo)
        token_info = AccessTokenInfo.model_validate(response.response_json)
        assert bearer == token_info.token_type
        decoded_jwt_refresh = decode_jwt(token_info.access_token)
        assert exist_user.id == decoded_jwt_refresh["sub"]
        assert exist_user.username == decoded_jwt_refresh["username"]
        assert ACCESS_TOKEN_TYPE == decoded_jwt_refresh[TOKEN_TYPE_FIELD]

    def test_refresh_invalid_token_type_401(
        self,
        client: FlaskClient,
        exist_user: UserOrm,
        jwt_access: Authorization,
    ):
        response = client.post(
            path=url_for(
                endpoint=refresh_endpoint,
            ),
            auth=jwt_access,
        )
        error_expectation = {
            "message": response_invalid_token_type_401.format(
                ACCESS_TOKEN_TYPE.__repr__(),
                REFRESH_TOKEN_TYPE.__repr__(),
            )
        }
        response = Response(response)
        response.assert_status_code(HTTP.UNAUTHORIZED_401)
        response.assert_data(error_expectation)
