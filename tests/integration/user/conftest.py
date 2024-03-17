import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_blog.config import Config
from fastapi_blog.entity.users.models import User
from fastapi_blog.entity.users.repository import UserRepository
from fastapi_blog.entity.users.service import UserService


@pytest.fixture(scope="session")
def user_gateway(session: AsyncSession):
    return UserRepository(session, User)


@pytest.fixture(scope="session")
def user_service(user_gateway: UserRepository, config: Config) -> UserService:
    return UserService(user_gateway, config.app.jwt_secret)
