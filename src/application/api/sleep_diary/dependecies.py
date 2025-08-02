from fastapi.security import HTTPBearer, OAuth2PasswordBearer


token_bearer_dependency = HTTPBearer(auto_error=False)
get_token_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login/")
