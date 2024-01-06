import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Generator, TypeAlias

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.app_setup import create_app, initialise_routers
from src.config import AppSettings, load_app_config
from src.database.base import Base
from src.database.dependencies import create_session
from src.database.sa_utils import create_session_maker
from src.entity.models import *  # noqa

BASE_URL = "http://test"

TEST_DOTENV_PATH = ".envs/test.env"
TEST_DB_PATH = "tests/test.db"
TEST_DB_DSN = f"sqlite+aiosqlite:///{TEST_DB_PATH}"

SessionMaker: TypeAlias = sessionmaker[AsyncSession]


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def config() -> AppSettings:
    return load_app_config(TEST_DOTENV_PATH)


@pytest.fixture(scope="session")
def app(config: AppSettings) -> FastAPI:
    app = create_app(config)
    initialise_routers(app)

    return app


@pytest_asyncio.fixture(scope="session")
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        yield ac


@pytest.fixture(scope="session")
def db_path() -> str:
    return TEST_DB_PATH


@pytest.fixture(scope="session")
def engine() -> AsyncEngine:
    return create_async_engine(TEST_DB_DSN, echo=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialise_test_db(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def session_factory(engine: AsyncEngine) -> SessionMaker:
    session_maker = create_session_maker(engine)
    return session_maker


@pytest.fixture(scope="session")
async def session(
        session_factory: SessionMaker,
) -> AsyncGenerator[AsyncSession, None]:
    async with create_session(session_factory) as session:
        yield session
