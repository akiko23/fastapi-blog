from functools import partial

from fastapi import APIRouter, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_blog.depends_stub import Stub
from fastapi_blog.entity.users.gateway import UserGateway
from fastapi_blog.config import BackendConfig
from fastapi_blog.consts import APP_DOTENV_PATH
from fastapi_blog.database.dependencies import get_session
from fastapi_blog.database.sa_utils import create_engine, create_session_maker
from fastapi_blog.dependencies import get_config
from fastapi_blog.entity.users.router import router as users_router

from fastapi_blog.entity.users.dependencies import get_user_gateway

router = APIRouter()


@router.get("/")
async def read_main():
    return {"msg": "Welcome to FastAPI-blog!"}


def initialise_routers(app: FastAPI) -> None:
    app.include_router(router)
    app.include_router(users_router)


def initialise_dependencies(app: FastAPI, config: BackendConfig) -> None:
    engine = create_engine(config.db.uri)
    session_factory = create_session_maker(engine)

    app.dependency_overrides[Stub(AsyncSession)] = partial(
        get_session, session_factory
    )
    app.dependency_overrides[Stub(BackendConfig)] = partial(
        get_config, APP_DOTENV_PATH
    )

    app.dependency_overrides[Stub(UserGateway)] = get_user_gateway


def create_app(config: BackendConfig) -> FastAPI:
    app = FastAPI(title=config.app.title, description=config.app.description)
    return app
