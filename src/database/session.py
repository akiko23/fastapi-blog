from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


async def create_session(session_factory: sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


def create_session_maker(db_uri: str):
    kw = {
        "url": db_uri,
        "echo": True,
        "connect_args": {
            "timeout": 5,
        }
    }
    if 'postgresql' in db_uri:
        kw.update(pool_size=15, max_overflow=15)

    engine = create_async_engine(**kw)
    return sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
