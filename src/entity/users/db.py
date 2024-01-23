from fastapi import Depends
from fastapi_users.db import BaseUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from depends_stub import Stub
from src.entity.users.models import User


async def get_user_db(session: AsyncSession = Depends(Stub(AsyncSession))) -> BaseUserDatabase:
    yield SQLAlchemyUserDatabase(session, User)
