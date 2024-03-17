from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_blog.config import Config
from fastapi_blog.depends_stub import Stub
from fastapi_blog.entity.users.models import User
from fastapi_blog.entity.users.repository import UserRepository
from fastapi_blog.entity.users.service import UserService


async def get_user_repository(
    session: AsyncSession = Depends(Stub(AsyncSession)),
) -> UserRepository:
    yield UserRepository(session, User)


async def get_user_service(
    user_repository: UserRepository = Depends(Stub(UserRepository)),
    config: Config = Depends(Stub(Config)),
) -> UserService:
    yield UserService(user_repository, config.app.jwt_secret)
