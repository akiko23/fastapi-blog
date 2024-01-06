from fastapi import Depends
from fastapi_users.db import BaseUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.stubs import get_session_stub
from src.entity.users.models import User


async def get_user_db(session: AsyncSession = Depends(get_session_stub)) -> BaseUserDatabase:
    yield SQLAlchemyUserDatabase(session, User)
