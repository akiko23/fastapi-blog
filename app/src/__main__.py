import asyncio
from functools import partial

from fastapi import FastAPI
import uvicorn

from src.database.session import create_session_maker, create_session
from src.dependencies import get_session_stub

from src.config import load_app_config, AppSettings


def initialise_routers(app: FastAPI) -> None:
    pass


def initialise_dependencies(app: FastAPI, config: AppSettings) -> None:
    session_factory = create_session_maker(db_uri=config.db_uri)
    app.dependency_overrides[get_session_stub] = partial(create_session, session_factory)


def create_app(config: AppSettings) -> FastAPI:
    app = FastAPI(
        title=config.app_title,
        description=config.app_description
    )
    return app


async def main():
    config = load_app_config('src/.env')
    app = create_app(config)

    initialise_routers(app)
    initialise_dependencies(app, config)

    uvicorn_config = uvicorn.Config(
        app,
        host=config.host,
        port=config.port,
        log_level=config.log_level
    )

    server = uvicorn.Server(uvicorn_config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
