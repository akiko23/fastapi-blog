from fastapi import APIRouter
from fastapi_users import fastapi_users

from src.entity.auth.router import authenticator
from src.entity.auth.user_manager import get_user_manager
from src.entity.users.schemas import UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(get_user_manager, UserRead, UserUpdate, authenticator),
    prefix="/users",
    tags=["users"],
)
