from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from cv_matcher.core.config import settings
from cv_matcher.core.database import Base, get_db
from cv_matcher.main import create_app

# NullPool: the app (via TestClient) and the async fixtures below run on
# different event loops. asyncpg connections are bound to the loop that
# created them, so pooling would hand a connection from one loop to
# another and crash. NullPool opens a fresh connection per checkout instead.
test_engine = create_async_engine(settings.test_database_url, poolclass=NullPool)
TestSessionFactory = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def _setup_database() -> AsyncGenerator[None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def _override_get_db() -> AsyncGenerator[AsyncSession]:
    async with TestSessionFactory() as session:
        yield session


@pytest.fixture
def client() -> Generator[TestClient]:
    app = create_app()
    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
