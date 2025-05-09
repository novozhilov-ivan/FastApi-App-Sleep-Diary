from pydantic_settings import BaseSettings


class TokenAuthSettings(BaseSettings):
    token_cookies_key: str = "authorization_token"
