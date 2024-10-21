from pydantic_settings import BaseSettings


class AuthJWTSettings(BaseSettings):
    PRIVATE_KEY: str
    PUBLIC_KEY: str
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
