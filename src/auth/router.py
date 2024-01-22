from fastapi import APIRouter, Depends
from fastapi_users import fastapi_users
from fastapi_users.authentication import (
    AuthenticationBackend,
    Authenticator,
    BearerTransport,
    JWTStrategy,
)

from src.config import BackendConfig
from src.auth.user_manager import get_user_manager
from src.entity.users.schemas import UserCreate, UserRead
from src.stubs import get_config_stub

router = APIRouter()


def get_jwt_strategy(config: BackendConfig = Depends(get_config_stub)) -> JWTStrategy:
    return JWTStrategy(secret=config.app.jwt_secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)
authenticator = Authenticator(backends=[auth_backend], get_user_manager=get_user_manager)

router.include_router(
    fastapi_users.get_auth_router(
        auth_backend,
        get_user_manager,
        authenticator,
    ), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(get_user_manager, UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(get_user_manager),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(get_user_manager, UserRead),
    prefix="/auth",
    tags=["auth"],
)
