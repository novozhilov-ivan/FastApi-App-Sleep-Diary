import pytest
from werkzeug.datastructures import Authorization

from api.extension import bearer
from api.models import User
from api.utils.jwt import create_refresh_jwt
from common.pydantic_schemas.user import UserValidate


@pytest.fixture
def jwt_refresh(exist_user: User) -> Authorization:
    user = UserValidate.model_validate(exist_user)
    yield Authorization(
        auth_type=bearer,
        token=create_refresh_jwt(user),
    )
