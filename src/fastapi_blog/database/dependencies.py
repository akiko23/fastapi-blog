from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from fastapi_blog.database.sa_utils import create_session


async def get_session(session_factory: sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with create_session(session_factory) as session:
        yield session
