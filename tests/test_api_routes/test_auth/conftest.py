import pytest

from api.models import User

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
