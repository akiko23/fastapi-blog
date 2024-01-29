from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_blog.config import BackendConfig
from fastapi_blog.depends_stub import Stub
from fastapi_blog.entity.users.gateway import UserGateway
from fastapi_blog.entity.users.models import User
from fastapi_blog.entity.users.service import UserService


async def get_user_gateway(session: AsyncSession = Depends(Stub(AsyncSession))) -> UserGateway:
    yield UserGateway(session, User)


async def get_user_service(
        user_gateway: UserGateway = Depends(Stub(UserGateway)),
        config: BackendConfig = Depends(Stub(BackendConfig))
):
    yield UserService(user_gateway, config.app.jwt_secret)
