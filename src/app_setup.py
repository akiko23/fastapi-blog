from functools import partial

from fastapi import APIRouter, FastAPI

from src.config import BackendConfig
from src.consts import APP_DOTENV_PATH
from src.database.dependencies import get_session
from src.database.sa_utils import create_engine, create_session_maker
from src.database.stubs import get_session_stub
from src.dependencies import get_config
from src.auth.router import router as auth_router
from src.stubs import get_config_stub

router = APIRouter()


@router.get("/")
async def read_main():
    return {"msg": "Welcome to FastAPI-blog!"}


def initialise_routers(app: FastAPI) -> None:
    app.include_router(router)
    app.include_router(auth_router)


def initialise_dependencies(app: FastAPI, config: BackendConfig) -> None:
    engine = create_engine(config.db.uri)
    session_factory = create_session_maker(engine)

    app.dependency_overrides[get_session_stub] = partial(
        get_session, session_factory
    )
    app.dependency_overrides[get_config_stub] = partial(
        get_config, APP_DOTENV_PATH
    )


def create_app(config: BackendConfig) -> FastAPI:
    app = FastAPI(title=config.app.title, description=config.app.description)
    return app
