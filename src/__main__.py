import asyncio

import uvicorn

from src.app_setup import (
    create_app,
    initialise_dependencies,
    initialise_routers,
)
from src.config import load_app_config
from src.consts import APP_DOTENV_PATH


async def main() -> None:
    config = load_app_config(APP_DOTENV_PATH)
    app = create_app(config)

    initialise_routers(app)
    initialise_dependencies(app, config)

    uvicorn_config = uvicorn.Config(
        app, host=config.host, port=config.port, log_level=config.log_level
    )

    server = uvicorn.Server(uvicorn_config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
