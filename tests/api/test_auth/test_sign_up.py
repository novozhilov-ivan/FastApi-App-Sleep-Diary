import pytest

from flask import url_for
from flask.testing import FlaskClient
from sqlalchemy import select

from src.extension import db
from src.models import UserOrm
from src.pydantic_schemas.user import (
    UserCredentials,
    UserValidate,
)
from src.routes.auth.sign_up import (
    response_conflict_409,
    response_created_201,
    signup_endpoint,
)
from src.utils.auth import validate_password
from src.utils.status_codes import HTTP
from tests.api.response import Response


@pytest.mark.auth
@pytest.mark.sign_up
class TestSignUp:
    content_type = "application/x-www-form-urlencoded"

    def test_sign_up_201(
        self,
        client: FlaskClient,
        user_credentials: UserCredentials,
    ):
        raw_response = client.post(
            path=url_for(
                endpoint=signup_endpoint,
            ),
            data=user_credentials.model_dump(),
            content_type=self.content_type,
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.CREATED_201)
        response.assert_data(response_created_201)

        with client.application.app_context():
            db_user = db.session.execute(select(UserOrm)).scalar_one_or_none()
        assert db_user
        assert user_credentials.username == db_user.username
        assert validate_password(
            password=user_credentials.password,
            hashed_password=db_user.password.encode(),
        )

    def test_sign_up_409(
        self,
        client: FlaskClient,
        user_credentials: UserCredentials,
        exist_user: UserValidate,
    ):
        raw_response = client.post(
            path=url_for(
                endpoint=signup_endpoint,
            ),
            data=user_credentials.model_dump(),
            content_type=self.content_type,
        )
        response = Response(raw_response)
        response.assert_status_code(HTTP.CONFLICT_409)
        error_expectation = {"message": response_conflict_409}
        response.assert_data(error_expectation)

    @pytest.mark.skip(reason="Тест отсутствует")
    def test_sign_up_422(self):
        pass
