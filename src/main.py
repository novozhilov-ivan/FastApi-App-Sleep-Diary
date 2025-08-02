from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, status

from src.application.api.identity.api.handlers.users import router as user_router
from src.application.api.schemas import ErrorSchema
from src.application.api.sleep_diary.handlers.about.handlers import (
    router as about_router,
)
from src.application.api.sleep_diary.handlers.notes.handlers import (
    router as notes_router,
)
from src.project.container import get_async_container


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sleep Diary",
        debug=True,
        responses={
            status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
        },
    )
    setup_dishka(
        container=get_async_container(),
        app=app,
    )

    app.include_router(about_router)
    app.include_router(notes_router)
    app.include_router(user_router)

    return app
