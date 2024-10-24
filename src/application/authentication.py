BEARER_TOKEN_TYPE: str = "Bearer"
AUTH_TYPE_OAUTH2: str = "OAuth2"
authorizations: dict[str, dict[str, str]] = {
    BEARER_TOKEN_TYPE: {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": (
            "Enter the token with the `Bearer` prefix, e.g. 'Bearer abcde12345'"
        ),
    },
    AUTH_TYPE_OAUTH2: {
        "type": "oauth2",
        "flow": "password",
        "tokenUrl": "api/login/",
        "authorizationUrl": "api/login/",
    },
}
