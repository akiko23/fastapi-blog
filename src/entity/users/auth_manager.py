from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, models
from fastapi_users.db import BaseUserDatabase
from fastapi_users.password import PasswordHelperProtocol

from depends_stub import Stub
from src.config import BackendConfig
from src.entity.users.db import get_user_db
from src.entity.users.models import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    def __init__(
            self,
            user_db: BaseUserDatabase[models.UP, models.ID],
            token_secret: str,
            password_helper: Optional[PasswordHelperProtocol] = None,
    ):
        self.reset_password_token_secret = token_secret
        self.verification_token_secret = token_secret

        super().__init__(user_db, password_helper)

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        if user.username is None:
            user.username = f"user{user.id}"
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(
    user_db: BaseUserDatabase = Depends(get_user_db),
    config: BackendConfig = Depends(Stub(BackendConfig))
):
    yield UserManager(user_db, config.app.jwt_secret)
