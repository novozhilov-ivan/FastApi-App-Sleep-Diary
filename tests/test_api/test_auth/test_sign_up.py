import pytest
from flask import url_for
from flask.testing import FlaskClient
from sqlalchemy import select

from api import db
from api.models import User
from api.routes.auth.sign_up import (
    response_conflict_409,
    response_created_201,
    signup_endpoint,
)
from api.utils.auth import validate_password
from common.baseclasses.response import Response
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserCredentials, UserValidate


@pytest.mark.auth
@pytest.mark.sign_up
class TestSignUp:
    content_type = "application/x-www-form-urlencoded"

    def test_sign_up_201(
        self,
        client: FlaskClient,
        user_credentials: UserCredentials,
    ):
        response = client.post(
            url_for(signup_endpoint),
            data=user_credentials.model_dump(),
            content_type=self.content_type,
        )
        response = Response(response)
        response.assert_status_code(HTTP.CREATED_201)
        response.assert_data(response_created_201)

        with client.application.app_context():
            db_user = db.session.execute(select(User)).scalar_one_or_none()
        assert user_credentials.username == db_user.username
        assert validate_password(
            password=user_credentials.password,
            hashed_password=db_user.password.encode(),
        )

    @pytest.mark.parametrize(
        "wrong_password",
        (
            {"password": "wrong".encode()},
            {"password": None},
        ),
    )
    def test_sign_up_409(
        self,
        client: FlaskClient,
        wrong_password: dict,
        user_credentials: UserCredentials,
        exist_db_user: UserValidate,
    ):
        wrong_password = wrong_password.get("password")
        if isinstance(wrong_password, bytes):
            user_credentials.password = wrong_password
        expectation = {
            "message": response_conflict_409,
        }
        response = client.post(
            url_for(signup_endpoint),
            data=user_credentials.model_dump(),
            content_type=self.content_type,
        )
        response = Response(response)
        response.assert_status_code(HTTP.CONFLICT_409)
        response.assert_data(expectation)
