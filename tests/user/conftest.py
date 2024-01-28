import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from config import BackendConfig
from src.entity.users.gateway import UserGateway
from src.entity.users.models import User
from src.entity.users.service import UserService


@pytest.fixture(scope="session")
def user_gateway(session: AsyncSession):
    return UserGateway(session, User)


@pytest.fixture(scope="session")
def user_service(user_gateway: UserGateway, config: BackendConfig) -> UserService:
    return UserService(user_gateway, config.app.jwt_secret)
