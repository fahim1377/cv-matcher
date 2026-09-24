from fastapi import FastAPI

from cv_matcher.api.health import router as health_router
from cv_matcher.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.include_router(health_router)
    return app


app = create_app()
