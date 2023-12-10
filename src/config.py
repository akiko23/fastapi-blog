import logging
import os
from dataclasses import dataclass
from typing import Optional, cast

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# You can replace this consts values with your own awesome ones :D
DEFAULT_TITLE: str = "fastapi-blog"
DEFAULT_DESCRIPTION: str = "A sample blog developed using FastAPI"
DEFAULT_HOST: str = "0.0.0.0"
DEFAULT_PORT: int = 8000
DEFAULT_LOG_LEVEL: str = "info"


class ConfigParseError(ValueError):
    pass


@dataclass
class AppSettings:
    app_title: str
    app_description: str
    host: str
    port: int
    log_level: str

    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int

    def __post_init__(self) -> None:
        self.db_uri = (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )


def get_env_var_or_err(name: str) -> str:
    var = os.getenv(name)
    if not var:
        logger.error("%s is not set", name)
        raise ConfigParseError(f"{name} is not set")
    return var


def load_app_config(dotenv_path: Optional[str] = None) -> AppSettings:
    load_dotenv(dotenv_path)

    # Optional args (have default values)
    app_title = os.getenv("APP_TITLE") or DEFAULT_TITLE
    app_description: str = os.getenv("APP_DESCRIPTION") or DEFAULT_DESCRIPTION
    host: str = os.getenv("HOST") or DEFAULT_HOST
    port: int = cast(int, os.getenv("PORT")) or DEFAULT_PORT
    log_level: str = os.getenv("LOG_LEVEL") or DEFAULT_LOG_LEVEL

    # Required args (if not in env file, an error occurs)
    db_user: str = get_env_var_or_err("DB_USER")
    db_password: str = get_env_var_or_err("DB_PASSWORD")
    db_name: str = get_env_var_or_err("DB_NAME")
    db_host: str = get_env_var_or_err("DB_HOST")
    db_port: int = int(get_env_var_or_err("DB_PORT"))

    return AppSettings(
        app_title,
        app_description,
        host,
        port,
        log_level,
        db_user,
        db_password,
        db_name,
        db_host,
        db_port,
    )
