from functools import wraps
from typing import Protocol, TypeVar

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse

from src.domain.identity.exceptions import IdentityError

R_co = TypeVar("R_co", bound=Response, covariant=True)


class IdentityErrorHandlerFunc(Protocol[R_co]):
    def __call__(self, request: Request, exc: IdentityError, /) -> R_co: ...


def ui_identity_error_handler[R_co](
    func: IdentityErrorHandlerFunc[R_co],
) -> IdentityErrorHandlerFunc[R_co]:
    @wraps(func)
    def wrapper(request: Request, exc: IdentityError) -> R_co:
        if request.url.path.startswith("/ui"):
            return RedirectResponse(
                url=request.url_for("fetch_sign_in_page").replace_query_params(
                    error=exc.message,
                ),
                status_code=status.HTTP_302_FOUND,
            )
        return func(request, exc)

    return wrapper


@ui_identity_error_handler
def identity_error_handler(request: Request, exc: IdentityError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.message},
    )
