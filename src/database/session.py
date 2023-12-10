from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


@asynccontextmanager
async def create_session(
    session_factory: sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


def create_session_maker(db_uri: str) -> sessionmaker[AsyncSession]:
    engine_extra_params = {
        "echo": True,
        "connect_args": {
            "timeout": 5,
        },
        "pool_size": 15,
        "max_overflow": 15,
    }
    if "test" in db_uri:
        # The engine of test db (sqlite) doesn't support this params
        engine_extra_params.update(pool_size=None, max_overflow=None)

    engine = create_async_engine(db_uri, **engine_extra_params)
    return sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )
