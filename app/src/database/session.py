from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


async def create_session(session_factory: sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


def create_session_maker(db_uri: str):
    engine = create_async_engine(
        db_uri,
        echo=True,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
