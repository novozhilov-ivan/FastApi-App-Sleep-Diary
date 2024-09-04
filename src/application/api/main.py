from fastapi import FastAPI

from src.application.api.routers import about


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sleep Diary",
        description="Sleep Diary description.",
        docs_url="/api/docs",
        debug=True,
    )
    app.include_router(about.router)
    app.include_router(about.router, prefix="/about")
    return app
