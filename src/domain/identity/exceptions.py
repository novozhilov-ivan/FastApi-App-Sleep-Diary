class IdentityError(Exception):
    @property
    def message(self) -> str:
        return "Неизвестная ошибка при авторизации/аутентификации."


class JWTError(IdentityError):
    @property
    def message(self) -> str:
        return "Невалидный токен."


class JWTDecodeError(JWTError):
    pass


class JWTExpiredError(JWTError):
    pass


class JWTEncodeError(JWTError):
    pass


class AccessTokenIsExpiredError(JWTError):
    pass


class UnauthorizedError(IdentityError):
    @property
    def message(self) -> str:
        return "Ошибка авторизации."


class CredentialsRequiredError(IdentityError):
    @property
    def message(self) -> str:
        return "Наличие Username обязательно."


class PasswordsMismatchError(IdentityError):
    @property
    def message(self) -> str:
        return "Пароли не совпадают."
