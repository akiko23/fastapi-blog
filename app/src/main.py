import asyncio

from fastapi import FastAPI
import uvicorn

from config import load_app_config

app = FastAPI(
    title='fastapi-blog',
    description='A sample blog developed using FastAPI'
)


async def main():
    config = load_app_config()

    uvicorn_config = uvicorn.Config(
        app,
        host=config.HOST,
        port=config.PORT,
        log_level=config.LOG_LEVEL
    )

    server = uvicorn.Server(uvicorn_config)
    await server.serve()


if __name__ == "__main__":
   asyncio.run(main()) 

