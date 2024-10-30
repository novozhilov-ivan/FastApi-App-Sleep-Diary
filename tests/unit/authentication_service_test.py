import pytest

from src.domain.entities import UserEntity
from src.domain.services import IUsersRepository
from src.domain.specifications import UserCredentialsSpecification
from src.infra.repository import MemoryUsersRepository
from src.service_layer.exceptions import (
    LogInException,
    NotAuthenticatedException,
    UserCredentialsFormatException,
    UserNameAlreadyExistException,
)
from src.service_layer.services import (
    IUserAuthenticationService,
    NotAuthenticated,
    UserAuthenticationService,
)


def test_property_user_authenticated(
    created_user: UserEntity,
    created_user_with_hashed_password: UserEntity,
    user_repository: IUsersRepository,
    authentication_service: IUserAuthenticationService,
):
    assert isinstance(authentication_service._user, NotAuthenticated)

    user_repository.add_user(created_user_with_hashed_password)
    authentication_service.login(created_user.username, created_user.password)

    assert isinstance(authentication_service._user, UserEntity)

    assert isinstance(authentication_service.user, UserEntity)
    assert authentication_service.user


def test_property_user_not_authenticated_exception(
    authentication_service: IUserAuthenticationService,
):
    assert isinstance(authentication_service._user, NotAuthenticated)

    with pytest.raises(NotAuthenticatedException):
        _ = authentication_service.user

    assert isinstance(authentication_service._user, NotAuthenticated)
    assert authentication_service._user == NotAuthenticated()


def test_login(
    created_user: UserEntity,
    created_user_with_hashed_password: UserEntity,
    user_repository: IUsersRepository,
    authentication_service: IUserAuthenticationService,
):
    user_repository.add_user(created_user_with_hashed_password)

    assert isinstance(authentication_service._user, NotAuthenticated)

    authentication_service.login(created_user.username, created_user.password)

    assert isinstance(authentication_service._user, UserEntity)
    assert authentication_service.user


def test_different_hashes_for_equals_passwords():
    first_password = second_password = "test_password"
    first_hash = UserAuthenticationService.hash_password(first_password)
    second_hash = UserAuthenticationService.hash_password(second_password)

    assert first_hash != second_hash


def test_compare_passwords(
    created_user: UserEntity,
    created_user_with_hashed_password: UserEntity,
):
    assert created_user.password != created_user_with_hashed_password.password

    assert UserAuthenticationService.compare_passwords(
        password=created_user.password,
        hashed_password=created_user_with_hashed_password.password,
    )


def test_validate_user_login_exception(
    created_user: UserEntity,
    created_user_with_hashed_password: UserEntity,
    user_repository: IUsersRepository,
    authentication_service: UserAuthenticationService,
):
    wrong_username = f"wrong_{created_user.username}"

    assert isinstance(authentication_service._user, NotAuthenticated)

    with pytest.raises(LogInException):
        authentication_service._validate_user(wrong_username)

    user_repository.add_user(created_user_with_hashed_password)

    with pytest.raises(LogInException):
        authentication_service._validate_user(wrong_username)

    assert isinstance(authentication_service._user, NotAuthenticated)


def test_validate_password_login_exception(
    created_user: UserEntity,
    created_user_with_hashed_password: UserEntity,
    user_repository: IUsersRepository,
    authentication_service: UserAuthenticationService,
):
    wrong_password = f"wrong_{created_user.password}"

    assert isinstance(authentication_service._user, NotAuthenticated)

    with pytest.raises(LogInException):
        authentication_service._validate_user_password(
            user=created_user_with_hashed_password,
            password=wrong_password,
        )

    user_repository.add_user(created_user_with_hashed_password)

    with pytest.raises(LogInException):
        authentication_service._validate_user_password(
            user=created_user_with_hashed_password,
            password=wrong_password,
        )

    assert isinstance(authentication_service._user, NotAuthenticated)


@pytest.mark.parametrize(
    "wrong_credentials",
    [
        {
            "username": "correct_username",
            "password": "wrong_password",
        },
        {
            "username": "wrong_username",
            "password": "correct_password",
        },
        {
            "username": "wrong_username",
            "password": "wrong_password",
        },
    ],
)
def test_bad_login_with_login_exception(
    wrong_credentials: dict,
    created_user_with_hashed_password: UserEntity,
    user_repository: IUsersRepository,
    authentication_service: IUserAuthenticationService,
):
    assert isinstance(authentication_service._user, NotAuthenticated)

    with pytest.raises(LogInException):
        authentication_service.login(
            username=wrong_credentials["username"],
            password=wrong_credentials["password"],
        )

    user_repository.add_user(created_user_with_hashed_password)

    with pytest.raises(LogInException):
        authentication_service.login(
            username=wrong_credentials["username"],
            password=wrong_credentials["password"],
        )

    assert isinstance(authentication_service._user, NotAuthenticated)


def test_get_user(
    created_user: UserEntity,
    created_user_with_hashed_password: UserEntity,
    user_repository: IUsersRepository,
    authentication_service: UserAuthenticationService,
):
    assert authentication_service._get_user(created_user.username) is None

    user_repository.add_user(created_user_with_hashed_password)
    user = authentication_service._get_user(created_user.username)

    assert isinstance(user, UserEntity)
    assert user == created_user_with_hashed_password == created_user


def test_correct_logout(
    created_user: UserEntity,
    created_user_with_hashed_password: UserEntity,
    user_repository: IUsersRepository,
    authentication_service: IUserAuthenticationService,
):
    assert isinstance(authentication_service._user, NotAuthenticated)

    user_repository.add_user(created_user_with_hashed_password)
    authentication_service.login(created_user.username, created_user.password)

    assert isinstance(authentication_service._user, UserEntity)
    assert authentication_service.user

    authentication_service.logout()

    assert isinstance(authentication_service._user, NotAuthenticated)


def test_cannot_logout_if_not_authenticated(
    authentication_service: IUserAuthenticationService,
):
    assert isinstance(authentication_service._user, NotAuthenticated)

    with pytest.raises(NotAuthenticatedException):
        authentication_service.logout()

    assert isinstance(authentication_service._user, NotAuthenticated)


def test_correct_register(
    created_user: UserEntity,
    user_repository: IUsersRepository,
    authentication_service: IUserAuthenticationService,
):
    assert user_repository.get_by_username(created_user.username) is None

    authentication_service.register(created_user.username, created_user.password)

    authentication_service.login(created_user.username, created_user.password)
    user = user_repository.get_by_username(created_user.username)

    assert isinstance(user, UserEntity)
    assert user == authentication_service.user == user == created_user


def test_register_username_already_exist_exception(
    created_user: UserEntity,
    user_repository: MemoryUsersRepository,
    authentication_service: IUserAuthenticationService,
):
    assert user_repository.get_by_username(created_user.username) is None

    authentication_service.register(created_user.username, created_user.password)

    with pytest.raises(UserNameAlreadyExistException):
        authentication_service.register(created_user.username, created_user.password)

    assert len(user_repository._saved_users) == 1


@pytest.mark.parametrize(
    "wrong_format_credentials",
    [
        {
            "username": "u" * UserCredentialsSpecification.MIN_LEN_USERNAME,
            "password": "correct_password",
        },
        {
            "username": "u" * UserCredentialsSpecification.MAX_LEN_USERNAME,
            "password": "correct_password",
        },
        {
            "username": "correct_username",
            "password": "p" * UserCredentialsSpecification.MIN_LEN_PASSWORD,
        },
        {
            "username": "correct_username",
            "password": "p" * UserCredentialsSpecification.MAX_LEN_PASSWORD,
        },
    ],
)
def test_register_user_credentials_format_exception(
    wrong_format_credentials: dict,
    created_user: UserEntity,
    user_repository: IUsersRepository,
    authentication_service: IUserAuthenticationService,
):
    assert user_repository.get_by_username(created_user.username) is None

    with pytest.raises(UserCredentialsFormatException):
        authentication_service.register(
            username=wrong_format_credentials["username"],
            password=wrong_format_credentials["password"],
        )

    assert user_repository.get_by_username(created_user.username) is None


def test_correct_unregister(
    created_user: UserEntity,
    user_repository: IUsersRepository,
    authentication_service: IUserAuthenticationService,
):
    assert user_repository.get_by_username(created_user.username) is None

    authentication_service.register(created_user.username, created_user.password)
    authentication_service.login(created_user.username, created_user.password)

    assert authentication_service.user == created_user

    authentication_service.unregister()

    assert user_repository.get_by_username(created_user.username) is None
