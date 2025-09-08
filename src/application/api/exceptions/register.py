from fastapi import FastAPI

from src.application.api.exceptions.handlers import identity_error_handler
from src.domain.identity.exceptions import IdentityError


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(IdentityError, identity_error_handler)
