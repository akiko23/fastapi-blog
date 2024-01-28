from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import BackendConfig
from src.depends_stub import Stub
from src.entity.users.gateway import UserGateway
from src.entity.users.models import User
from src.entity.users.service import UserService


async def get_user_gateway(session: AsyncSession = Depends(Stub(AsyncSession))) -> UserGateway:
    yield UserGateway(session, User)


async def get_user_service(
        user_gateway: UserGateway = Depends(Stub(UserGateway)),
        config: BackendConfig = Depends(Stub(BackendConfig))
):
    yield UserService(user_gateway, config.app.jwt_secret)
