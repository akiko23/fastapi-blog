import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_blog.config import Config
from fastapi_blog.entity.users.models import User
from fastapi_blog.entity.users.repository import UserRepository
from fastapi_blog.entity.users.service import UserService


@pytest.fixture(scope="session")
def user_service(session: AsyncSession, config: Config) -> UserService:
    return UserService(UserRepository(session, User), config.app.jwt_secret)
