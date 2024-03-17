from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


@asynccontextmanager
async def create_session(
    session_factory: async_sessionmaker[AsyncSession],
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
    return create_async_engine(db_uri, **engine_options)


def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, autoflush=True, expire_on_commit=False)
