from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.domain.identity.entities import AccessTokenClaims
from src.domain.identity.jwt_processor import IJWTProcessor, JWTProcessor
from src.domain.identity.types import JWTClaims, JWTToken, TokenType
from src.domain.sleep_diary.services.base import IUsersRepository
from src.infra.identity.access_token_processor import AccessTokenProcessor
from src.infra.identity.authentication import (
    IUserAuthenticationService,
    UserAuthenticationService,
)
from src.project.settings import JWTSettings


@pytest.fixture(scope="session")
def authentication_service(
    repository: IUsersRepository,
) -> IUserAuthenticationService:
    return UserAuthenticationService(repository=repository)


@pytest.fixture(scope="session")
def jwt_settings() -> JWTSettings:
    return JWTSettings()


@pytest.fixture(scope="session")
def subject() -> str:
    return "test_subject"


@pytest.fixture(scope="session")
def issued_at() -> int:
    return int(datetime.now(UTC).timestamp())


@pytest.fixture(scope="session")
def expired_at(issued_at: int, jwt_settings: JWTSettings) -> int:
    return int(datetime.now(UTC).timestamp()) + jwt_settings.access_token_expire


@pytest.fixture(scope="session")
def jwt_token_ident() -> str:
    return str(uuid4())


@pytest.fixture(scope="session")
def claims(
    subject: str,
    username: str,
    issued_at: int,
    expired_at: int,
    jwt_token_ident: str,
) -> AccessTokenClaims:
    return AccessTokenClaims(
        subject=subject,
        issued_at=issued_at,
        expired_at=expired_at,
        token_type=TokenType.ACCESS,
        jwt_token_ident=jwt_token_ident,
        username=username,
    )


@pytest.fixture(scope="session")
def claims_payload(claims: AccessTokenClaims) -> JWTClaims:
    return claims.as_dict()


@pytest.fixture(scope="session")
def expired_jwt_token(
    claims: AccessTokenClaims,
    jwt_processor: IJWTProcessor,
) -> JWTToken:
    expired_claims_payload = claims.as_dict()
    expired_claims_payload["exp"] = 0
    return jwt_processor.encode(expired_claims_payload)


@pytest.fixture(scope="session")
def jwt_token(jwt_processor: IJWTProcessor, claims_payload: JWTClaims) -> JWTToken:
    return jwt_processor.encode(payload=claims_payload)


@pytest.fixture(scope="session")
def jwt_processor(jwt_settings: JWTSettings) -> IJWTProcessor:
    return JWTProcessor(jwt_settings=jwt_settings)


@pytest.fixture(scope="session")
def access_token_processor(jwt_processor: IJWTProcessor) -> AccessTokenProcessor:
    return AccessTokenProcessor(jwt_processor=jwt_processor)
