import logging
import os
from dataclasses import dataclass
from types import NoneType
from typing import Any, Optional, TypeVar

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# You can replace this consts values with your own awesome ones :D
DEFAULT_APP_TITLE: str = "fastapi-blog"
DEFAULT_APP_DESCRIPTION: str = "A sample blog developed using FastAPI"
DEFAULT_SERVER_HOST: str = "0.0.0.0"
DEFAULT_SERVER_PORT: int = 8000
DEFAULT_SERVER_LOG_LEVEL: str = "info"

T = TypeVar("T")


class ConfigParseError(ValueError):
    pass


def get_env_var_or_err(name: str) -> str:
    var = os.getenv(name)
    if not var:
        logger.error("%s is not set", name)
        raise ConfigParseError(f"{name} is not set")
    return var


def cast_var(type_: type[T], name: str, value: Any) -> T:
    try:
        return type_(value)
    except (TypeError, ValueError):
        var_type = type(value)
        if var_type is NoneType:
            return None

        logger.error("Type of %s must be %s, not %s", name, type_, var_type)
        raise ConfigParseError(f"Type of {name} must be {type_.__name__}, not {var_type.__name__}")


@dataclass
class AppConfig:
    title: str
    description: str
    jwt_secret: str


@dataclass
class HttpServerConfig:
    host: str
    port: int
    log_level: str


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
class BackendConfig:
    app: AppConfig
    http_server: HttpServerConfig
    db: Database


def load_app_config(dotenv_path: Optional[str] = None) -> BackendConfig:
    load_dotenv(dotenv_path)

    return BackendConfig(
        app=AppConfig(
            title=os.getenv("APP_TITLE", DEFAULT_APP_TITLE),
            description=os.getenv("APP_DESCRIPTION", DEFAULT_APP_DESCRIPTION),
            jwt_secret=get_env_var_or_err("JWT_SECRET"),
        ),
        http_server=HttpServerConfig(
            host=os.getenv("APP_HOST", DEFAULT_SERVER_HOST),
            port=cast_var(int, "APP_PORT", os.getenv("APP_PORT", DEFAULT_SERVER_PORT)),
            log_level=os.getenv("APP_LOG_LEVEL", DEFAULT_SERVER_LOG_LEVEL),
        ),
        db=Database(
            user=get_env_var_or_err("DB_USER"),
            password=get_env_var_or_err("DB_PASSWORD"),
            name=get_env_var_or_err("DB_NAME"),
            host=get_env_var_or_err("DB_HOST"),
            port=cast_var(int, "DB_PORT", get_env_var_or_err("DB_PORT")),
        )
    )
