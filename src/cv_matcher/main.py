from fastapi import FastAPI

from cv_matcher.api.auth import router as auth_router
from cv_matcher.api.cv import router as cv_router
from cv_matcher.api.health import router as health_router
from cv_matcher.api.jobs import router as jobs_router
from cv_matcher.api.matches import router as matches_router
from cv_matcher.api.users import router as users_router
from cv_matcher.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(cv_router)
    app.include_router(jobs_router)
    app.include_router(matches_router)
    return app


app = create_app()
