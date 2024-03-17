import logging
from dataclasses import dataclass

import toml

logger = logging.getLogger(__name__)

# You can replace this consts values with your own awesome ones :D
DEFAULT_APP_TITLE: str = "fastapi-blog"
DEFAULT_APP_DESCRIPTION: str = "A sample blog developed using FastAPI"
DEFAULT_SERVER_HOST: str = "0.0.0.0"
DEFAULT_SERVER_PORT: int = 8000
DEFAULT_SERVER_LOG_LEVEL: str = "info"


@dataclass(kw_only=True)  # type: ignore[call-overload]
class AppConfig:
    title: str = DEFAULT_APP_TITLE
    description: str = DEFAULT_APP_DESCRIPTION
    jwt_secret: str  # type: ignore[misc]


@dataclass
class HttpServerConfig:
    host: str = DEFAULT_SERVER_HOST
    port: int = DEFAULT_SERVER_PORT
    log_level: str = DEFAULT_SERVER_LOG_LEVEL


@dataclass
class Database:
    user: str
    password: str
    name: str
    host: str
    port: int

    def __post_init__(self) -> None:
        self.uri = (
            f"postgresql+asyncpg://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.name}"
        )


@dataclass
class Config:
    app: AppConfig
    http_server: HttpServerConfig
    db: Database


def load_config(config_path: str) -> Config:
    with open(config_path, "r") as config_file:
        data = toml.load(config_file)
    return Config(
        app=AppConfig(**data["app"]),
        http_server=HttpServerConfig(**data["http_server"]),
        db=Database(**data["db"]),
    )
