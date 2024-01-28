from fastapi import APIRouter, Depends
from fastapi_users import fastapi_users
from fastapi_users.authentication import (
    AuthenticationBackend,
    Authenticator,
    BearerTransport,
    JWTStrategy,
)

from depends_stub import Stub
from src.config import BackendConfig
from src.entity.users.dependencies import get_user_service
from src.entity.users.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users")


def get_jwt_strategy(config: BackendConfig = Depends(Stub(BackendConfig))) -> JWTStrategy:
    return JWTStrategy(secret=config.app.jwt_secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="users/auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)
authenticator = Authenticator(backends=[auth_backend], get_user_manager=get_user_service)

router.include_router(
    fastapi_users.get_users_router(get_user_service, UserRead, UserUpdate, authenticator),
    tags=["users"],
)

router.include_router(
    fastapi_users.get_auth_router(
        auth_backend,
        get_user_service,
        authenticator,
    ), prefix="/auth/jwt", tags=["users"]
)

router.include_router(
    fastapi_users.get_register_router(get_user_service, UserRead, UserCreate),
    prefix="/auth",
    tags=["users"],
)

router.include_router(
    fastapi_users.get_reset_password_router(get_user_service),
    prefix="/auth",
    tags=["users"],
)

router.include_router(
    fastapi_users.get_verify_router(get_user_service, UserRead),
    prefix="/auth",
    tags=["users"],
)
