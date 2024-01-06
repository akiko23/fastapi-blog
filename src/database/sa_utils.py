from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker


@asynccontextmanager
async def create_session(
        session_factory: sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


def create_engine(db_uri: str) -> AsyncEngine:
    engine_options = {
        "echo": True,
        "connect_args": {
            "timeout": 5,
        },
        "pool_size": 15,
        "max_overflow": 15,
    }
    if "test" in db_uri:
        # The engine of test db (sqlite) doesn't support this params
        engine_options.update(pool_size=None, max_overflow=None)

    return create_async_engine(db_uri, **engine_options)


def create_session_maker(engine: AsyncEngine) -> sessionmaker[AsyncSession]:
    return sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )
