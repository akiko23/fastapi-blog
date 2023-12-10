import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Generator, TypeAlias

import pytest
import pytest_asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.app_setup import create_app
from src.config import AppSettings, load_app_config
from src.database.base import Base
from src.database.session import create_session, create_session_maker
from src.entity.models import *  # noqa

TEST_DOTENV_PATH = "tests/.env"
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
async def app(config: AppSettings) -> AsyncGenerator[FastAPI, None]:
    app = create_app(config)

    uvicorn_config = uvicorn.Config(
        app, host=config.host, port=config.port, log_level=config.log_level
    )

    server = uvicorn.Server(uvicorn_config)

    await server.serve()
    yield app
    await server.shutdown()


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def db_path() -> str:
    return TEST_DB_PATH


@pytest.fixture(scope="session")
def engine() -> AsyncEngine:
    engine = create_async_engine(TEST_DB_DSN, echo=False)
    return engine


@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialise_test_db(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def session_factory() -> SessionMaker:
    session_maker = create_session_maker(TEST_DB_DSN)
    return session_maker


@pytest.fixture(scope="session")
async def override_session(
    session_factory: SessionMaker,
) -> AsyncGenerator[AsyncSession, None]:
    async with create_session(session_factory) as session:
        yield session
