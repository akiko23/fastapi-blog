import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_blog.config import BackendConfig
from fastapi_blog.entity.users.gateway import UserGateway
from fastapi_blog.entity.users.models import User
from fastapi_blog.entity.users.service import UserService


@pytest.fixture(scope="session")
def user_gateway(session: AsyncSession):
    return UserGateway(session, User)


@pytest.fixture(scope="session")
def user_service(user_gateway: UserGateway, config: BackendConfig) -> UserService:
    return UserService(user_gateway, config.app.jwt_secret)
