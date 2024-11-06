from fastapi import Depends, FastAPI
from starlette import status

from src.application.api.dependecies import token_bearer_dependency
from src.application.api.routers import about, auth, notes
from src.application.api.schemas import ErrorSchema


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sleep Diary",
        description="Sleep Diary description.",
        docs_url="/api/docs",
        debug=True,
        responses={
            status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
        },
    )
    app.include_router(about.router)
    app.include_router(about.router, prefix="/about")
    app.include_router(notes.router, prefix="/notes")
    app.include_router(auth.router_login, prefix="/auth")
    app.include_router(
        auth.router_me,
        prefix="/auth",
        dependencies=[Depends(token_bearer_dependency)],
    )
    app.include_router(auth.router_register, prefix="/auth")
    return app
