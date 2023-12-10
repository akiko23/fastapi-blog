from functools import partial

from fastapi import FastAPI, APIRouter

from src.config import AppSettings
from src.database.session import create_session, create_session_maker
from src.dependencies import get_session_stub

router = APIRouter()


@router.get("/")
async def read_main():
    return {"msg": "Welcome to FastAPI-blog!"}


def initialise_routers(app: FastAPI) -> None:
    app.include_router(router)


def initialise_dependencies(app: FastAPI, config: AppSettings) -> None:
    session_factory = create_session_maker(db_uri=config.db_uri)
    app.dependency_overrides[get_session_stub] = partial(
        create_session, session_factory
    )


def create_app(config: AppSettings) -> FastAPI:
    app = FastAPI(title=config.app_title, description=config.app_description)
    return app
