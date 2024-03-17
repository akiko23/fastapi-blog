from functools import partial

import uvicorn
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_blog.config import AppConfig, Config, HttpServerConfig
from fastapi_blog.database.dependencies import get_session
from fastapi_blog.database.sa_utils import create_engine, create_session_maker
from fastapi_blog.depends_stub import Stub
from fastapi_blog.entity.users.dependencies import get_user_service
from fastapi_blog.entity.users.router import router as users_router
from fastapi_blog.entity.users.service import UserService

router = APIRouter()


class MsgResponse(BaseModel):
    msg: str


@router.get("/")
async def read_main() -> MsgResponse:
    return MsgResponse(msg="Welcome to FastAPI-blog!")


def initialise_routers(app: FastAPI) -> None:
    app.include_router(router)
    app.include_router(users_router)


def initialise_dependencies(app: FastAPI, config: Config) -> None:
    engine = create_engine(config.db.uri)
    session_factory = create_session_maker(engine)

    app.dependency_overrides[Stub(AsyncSession)] = partial(get_session, session_factory)
    app.dependency_overrides[Stub(Config)] = lambda: config
    app.dependency_overrides[Stub(UserService)] = get_user_service


def create_app(app_cfg: AppConfig) -> FastAPI:
    app = FastAPI(title=app_cfg.title, description=app_cfg.description)
    return app


def create_http_server(
    app: FastAPI, http_server_cfg: HttpServerConfig
) -> uvicorn.Server:
    uvicorn_config = uvicorn.Config(
        app,
        host=http_server_cfg.host,
        port=http_server_cfg.port,
        log_level=http_server_cfg.log_level,
    )
    return uvicorn.Server(uvicorn_config)
