from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.application.api.router import router as api_router
from src.project.containers import get_container


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sleep Diary",
        debug=False,
        openapi_url=None,
        docs_url=None,
        redoc_url=None,
    )
    app.include_router(api_router)
    return app


def create_production_app() -> FastAPI:
    app = create_app()
    setup_dishka(
        container=get_container(),
        app=app,
    )
    return app
