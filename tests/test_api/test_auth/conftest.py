import pytest

from api.extension import bearer
from api.models import User
from api.utils.jwt import create_access_token, create_refresh_token
from common.pydantic_schemas.user import UserValidate

user_password_is_hashed = True
exist_db_user_indirect_params = (user_password_is_hashed,)
user_password_is_hashed_description = [
    f"User pwd is {'' if pwd_hashed else 'UN'}hashed"
    for pwd_hashed in exist_db_user_indirect_params
]


@pytest.fixture(
    name="exist_db_user",
    params=exist_db_user_indirect_params,
    ids=user_password_is_hashed_description,
)
def create_db_user(exist_db_user: User):
    return exist_db_user


@pytest.fixture
def access_token_header(exist_db_user: User) -> dict:
    user = UserValidate.model_validate(exist_db_user)
    yield {"Authorization": f"{bearer} {create_access_token(user)}"}


@pytest.fixture
def refresh_token_header(exist_db_user: User) -> dict:
    user = UserValidate.model_validate(exist_db_user)
    yield {"Authorization": f"{bearer} {create_refresh_token(user)}"}
