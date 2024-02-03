import asyncio

from fastapi_blog.app_setup import (
    create_app,
    initialise_dependencies,
    initialise_routers,
)
from fastapi_blog.config import load_config
from fastapi_blog.consts import CONFIG_PATH
from src.fastapi_blog.app_setup import create_http_server


async def main() -> None:
    config = load_config(CONFIG_PATH)
    app = create_app(config.app)

    initialise_routers(app)
    initialise_dependencies(app, config)

    server = create_http_server(app, config.http_server)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
