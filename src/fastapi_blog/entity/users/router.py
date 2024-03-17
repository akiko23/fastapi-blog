from fastapi import APIRouter, Depends
from fastapi_users.authentication import (
    AuthenticationBackend,
    Authenticator,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.fastapi_users import (  # type: ignore[attr-defined]
    get_auth_router,
    get_register_router,
    get_users_router,
)
from fastapi_users.router import get_reset_password_router, get_verify_router

from fastapi_blog.config import Config
from fastapi_blog.depends_stub import Stub
from fastapi_blog.entity.users.dependencies import get_user_service
from fastapi_blog.entity.users.models import User
from fastapi_blog.entity.users.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users")


def get_jwt_strategy(config: Config = Depends(Stub(Config))) -> JWTStrategy[User, int]:
    return JWTStrategy(secret=config.app.jwt_secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="users/auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)
authenticator = Authenticator(
    backends=[auth_backend], get_user_manager=get_user_service
)

router.include_router(
    get_users_router(get_user_service, UserRead, UserUpdate, authenticator),
    tags=["users"],
)

router.include_router(
    get_auth_router(
        auth_backend,
        get_user_service,
        authenticator,
    ),
    prefix="/auth/jwt",
    tags=["users"],
)

router.include_router(
    get_register_router(get_user_service, UserRead, UserCreate),
    prefix="/auth",
    tags=["users"],
)

router.include_router(
    get_reset_password_router(get_user_service),
    prefix="/auth",
    tags=["users"],
)

router.include_router(
    get_verify_router(get_user_service, UserRead),
    prefix="/auth",
    tags=["users"],
)
