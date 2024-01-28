import asyncio
import subprocess
import time
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

from src.app_setup import create_app, initialise_routers, initialise_dependencies
from src.config import BackendConfig, load_app_config
from src.database.dependencies import create_session
from src.database.sa_utils import create_session_maker
from src.database.base import Base
from src.entity.models import *  # noqa

BASE_URL = "http://test"
TEST_DOTENV_PATH = ".envs/test.env"

SessionMaker: TypeAlias = sessionmaker[AsyncSession]


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def config() -> BackendConfig:
    return load_app_config(TEST_DOTENV_PATH)


@pytest.fixture(scope="session")
def app(config: BackendConfig) -> FastAPI:
    app = create_app(config)
    initialise_routers(app)
    initialise_dependencies(app, config)
    return app


@pytest_asyncio.fixture(scope="session")
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url=BASE_URL, headers={"Accept": "application/json"}) as ac:
        yield ac


@pytest.fixture(scope="session")
def initialise_test_db(config: BackendConfig) -> None:
    subprocess.run("docker run "
                   "--name pgsql-test "
                   f"-e POSTGRES_USER={config.db.user} "
                   f"-e POSTGRES_PASSWORD={config.db.password} "
                   f"-e POSTGRES_DB={config.db.name} "
                   f"-p {config.db.port}:5432 "
                   "-d postgres")
    time.sleep(2)  # waiting until the database is ready to accept connections
    yield
    subprocess.run("docker stop pgsql-test")
    subprocess.run("docker rm pgsql-test")


@pytest.fixture(scope="session")
def engine(config: BackendConfig, initialise_test_db: ...) -> AsyncEngine:
    return create_async_engine(config.db.uri, echo=True)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialise_migrations(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def session_factory(engine: AsyncEngine) -> SessionMaker:
    session_maker = create_session_maker(engine)
    return session_maker


@pytest_asyncio.fixture(scope="session")
async def session(
        session_factory: SessionMaker,
) -> AsyncGenerator[AsyncSession, None]:
    async with create_session(session_factory) as async_session:
        yield async_session
