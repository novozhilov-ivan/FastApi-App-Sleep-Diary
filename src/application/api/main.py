from fastapi import FastAPI
from starlette import status

from src.application.api.routers import about, notes
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
    return app
