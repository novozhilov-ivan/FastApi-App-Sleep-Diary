bearer: str = "Bearer"
oauth2: str = "OAuth2"
authorizations: dict[str, dict[str, str]] = {
    bearer: {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": (
            "Enter the token with the `Bearer` prefix, e.g. 'Bearer abcde12345'"
        ),
    },
    oauth2: {
        "type": "oauth2",
        "flow": "password",
        "tokenUrl": "api/signin",
        "authorizationUrl": "api/signin",
    },
}
