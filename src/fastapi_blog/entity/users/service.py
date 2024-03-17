from typing import Optional

from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.password import PasswordHelperProtocol

from fastapi_blog.entity.users.models import User
from fastapi_blog.entity.users.repository import UserRepository


class UserService(IntegerIDMixin, BaseUserManager[User, int]):
    def __init__(
        self,
        user_db: UserRepository,
        token_secret: str,
        password_helper: Optional[PasswordHelperProtocol] = None,
    ) -> None:
        self.reset_password_token_secret = token_secret
        self.verification_token_secret = token_secret

        super().__init__(user_db, password_helper)

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        if user.username is None:
            user.username = f"user{user.id}"
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        print(f"Verification requested for user {user.id}. Verification token: {token}")
