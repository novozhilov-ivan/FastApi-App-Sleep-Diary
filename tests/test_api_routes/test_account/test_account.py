import pytest
from flask import url_for
from flask.testing import FlaskClient

from api.extension import bearer
from api.models import User
from api.routes.account import account_endpoint
from api.utils.jwt import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    response_invalid_authorization_token_401,
    response_invalid_token_type_401,
)
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserInfo, UserValidate
from tests.test_api_routes.test_auth.conftest import (
    exist_db_user_indirect_params,
    user_password_is_hashed,
    user_password_is_hashed_description,
)


@pytest.mark.parametrize(
    "exist_db_user",
    exist_db_user_indirect_params,
    indirect=user_password_is_hashed,
    ids=user_password_is_hashed_description,
)
class TestAccountInfo:

    def test_account_info_200(
        self,
        client: FlaskClient,
        exist_db_user: User,
    ):
        user = UserValidate.model_validate(exist_db_user)
        response = client.get(
            url_for(account_endpoint),
            headers={"Authorization": f"{bearer} {create_access_token(user)}"},
        )
        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        response.validate(UserInfo)
        expectation = UserInfo.model_validate(exist_db_user)
        response.assert_data(expectation)

    @pytest.mark.account_401
    def test_account_info_invalid_token_type_401(
        self,
        client: FlaskClient,
        exist_db_user: User,
    ):
        user = UserValidate.model_validate(exist_db_user)
        response = client.get(
            url_for(account_endpoint),
            headers={"Authorization": f"{bearer} {create_refresh_token(user)}"},
        )
        response = Response(response)
        response.assert_status_code(HTTP.UNAUTHORIZED_401)
        expectation = {
            "message": response_invalid_token_type_401.format(
                REFRESH_TOKEN_TYPE.__repr__(),
                ACCESS_TOKEN_TYPE.__repr__(),
            )
        }
        response.assert_data(expectation)

    @pytest.mark.account_401
    def test_account_info_invalid_token_without_headers_401(
        self,
        client: FlaskClient,
        exist_db_user: User,
    ):
        response = client.get(url_for(account_endpoint))
        response = Response(response)
        response.assert_status_code(HTTP.UNAUTHORIZED_401)
        expectation = {
            "message": response_invalid_authorization_token_401,
        }
        response.assert_data(expectation)

    @pytest.mark.account_401
    def test_account_info_invalid_token_wrong_user_401(
        self,
        client: FlaskClient,
        exist_db_user: User,
    ):
        user = UserValidate.model_validate(exist_db_user)
        user.id = 888
        response = client.get(
            url_for(account_endpoint),
            headers={"Authorization": f"{bearer} {create_access_token(user)}"},
        )
        response = Response(response)
        response.assert_status_code(HTTP.UNAUTHORIZED_401)
        expectation = {"message": response_invalid_authorization_token_401}
        response.assert_data(expectation)
