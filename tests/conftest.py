import asyncio

import pytest
import pytest_asyncio
import uvicorn
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.config import AppSettings, load_app_config
from src.database.base import Base
from src.entity.models import *  # noqa
from src.database.session import create_session, create_session_maker

TEST_DOTENV_PATH = 'tests/.env'
TEST_DB_PATH = 'tests/test.db'

TEST_DB_DSN = f'sqlite+aiosqlite:///{TEST_DB_PATH}'


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def db_path():
    return TEST_DB_PATH


@pytest.fixture(scope='session')
def config():
    return load_app_config(TEST_DOTENV_PATH)


@pytest.fixture(scope='session')
async def app(config: AppSettings):
    uvicorn_config = uvicorn.Config(
        app,
        host=config.host,
        port=config.port,
        log_level=config.log_level
    )

    server = uvicorn.Server(uvicorn_config)

    await server.serve()
    yield app
    await server.shutdown()


@pytest.fixture(scope='session')
def engine():
    engine = create_async_engine(TEST_DB_DSN, echo=False)
    return engine


@pytest_asyncio.fixture(scope='session', autouse=True)
async def initialise_test_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session')
def session_factory():
    session_maker = create_session_maker(TEST_DB_DSN)
    return session_maker


@pytest.fixture(scope='session')
async def override_session(session_factory: sessionmaker):
    async with create_session(session_factory) as session:
        yield session
