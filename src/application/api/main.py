from fastapi import FastAPI

from src.application.api.routers import diary_description


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sleep Diary",
        description="Sleep Diary description.",
        docs_url="/api/docs",
        debug=True,
    )
    app.include_router(diary_description.router)
    app.include_router(diary_description.router, prefix="/description")
    return app
