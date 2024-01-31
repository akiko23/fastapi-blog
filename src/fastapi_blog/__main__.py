import asyncio

import uvicorn

from fastapi_blog.app_setup import (
    create_app,
    initialise_dependencies,
    initialise_routers,
)
from fastapi_blog.config import load_app_config
from fastapi_blog.consts import APP_DOTENV_PATH

from src.fastapi_blog.app_setup import create_http_server


async def main() -> None:
    config = load_app_config(APP_DOTENV_PATH)
    app = create_app(config.app)

    initialise_routers(app)
    initialise_dependencies(app, config)

    server = create_http_server(app, config.http_server)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
