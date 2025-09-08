from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.domain.identity.exceptions import IdentityError


def identity_error_handler(_: Request, exc: IdentityError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.message},
    )
