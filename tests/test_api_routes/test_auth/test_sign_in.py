import pytest
from flask import url_for
from flask.testing import FlaskClient

from api.models import User
from api.routes.auth.sign_in import signin_endpoint
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.token import TokenInfo
from common.pydantic_schemas.user import UserCredentials


@pytest.mark.auth
@pytest.mark.sign_in
class TestSignIn:

    user_password_is_hashed = True
    indirect_params = (True,)
    user_password_is_hashed_info = [
        f"User pwd is {'' if prefix else 'UN'}hashed" for prefix in indirect_params
    ]

    @pytest.mark.parametrize(
        "exist_db_user",
        indirect_params,
        indirect=True,
        ids=user_password_is_hashed_info,
    )
    def test_sign_in_200(
        self,
        client: FlaskClient,
        exist_db_user: User,
    ):
        user = UserCredentials.model_validate(exist_db_user)
        user.password = "test_password".encode()
        response = client.post(
            url_for(signin_endpoint),
            data=user.model_dump(),
            content_type="application/x-www-form-urlencoded",
        )
        response = Response(response)
        response.assert_status_code(HTTP.OK_200)
        # TODO декодировать и проверить токены
        response.validate(TokenInfo)
