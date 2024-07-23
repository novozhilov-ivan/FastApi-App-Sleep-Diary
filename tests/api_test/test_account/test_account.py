import pytest

from flask import url_for
from flask.testing import FlaskClient
from werkzeug.datastructures import Authorization

from src.extension import bearer
from src.models import UserOrm
from src.pydantic_schemas.user import (
    UserInfo,
    UserValidate,
)
from src.routes.account import account_endpoint
from src.routes.account.account_find import response_not_found_404
from src.utils.jwt import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    create_access_jwt,
    response_invalid_authorization_token_401,
    response_invalid_token_type_401,
)
from src.utils.status_codes import HTTP
from tests.api_test.response import Response


@pytest.mark.account
@pytest.mark.account_find
class TestAccountFind:

    @pytest.mark.account_find_200
    def test_account_find_200(
        self,
        client: FlaskClient,
        exist_user: UserOrm,
        jwt_access: Authorization,
    ):
        raw_response = client.get(
            path=url_for(
                endpoint=account_endpoint,
            ),
            auth=jwt_access,
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(UserInfo)
        expectation = UserInfo.model_validate(exist_user)
        response.assert_data(expectation)

    @pytest.mark.account_401
    def test_account_info_invalid_token_type_401(
        self,
        client: FlaskClient,
        exist_user: UserOrm,
        jwt_refresh: Authorization,
    ):
        raw_response = client.get(
            path=url_for(
                endpoint=account_endpoint,
            ),
            auth=jwt_refresh,
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.UNAUTHORIZED_401)
        error_expectation = {
            "message": response_invalid_token_type_401.format(
                REFRESH_TOKEN_TYPE.__repr__(),
                ACCESS_TOKEN_TYPE.__repr__(),
            ),
        }
        response.assert_data(error_expectation)

    @pytest.mark.account_401
    def test_account_info_invalid_token_without_headers_401(
        self,
        client: FlaskClient,
        exist_user: UserOrm,
    ):
        raw_response = client.get(
            path=url_for(
                endpoint=account_endpoint,
            ),
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.UNAUTHORIZED_401)
        error_expectation = {"message": response_invalid_authorization_token_401}
        response.assert_data(error_expectation)

    @pytest.mark.account_404
    def test_account_info_user_not_found_404(
        self,
        client: FlaskClient,
        exist_user: UserOrm,
    ):
        user = UserValidate.model_validate(exist_user)
        user.id = 888
        jwt_with_wrong_user_id = Authorization(
            auth_type=bearer,
            token=create_access_jwt(user),
        )
        raw_response = client.get(
            path=url_for(
                endpoint=account_endpoint,
            ),
            auth=jwt_with_wrong_user_id,
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.NOT_FOUND_404)
        error_expectation = {"message": response_not_found_404}
        response.assert_data(error_expectation)
