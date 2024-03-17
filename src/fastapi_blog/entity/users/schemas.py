from datetime import datetime
from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    username: str
    registered_at: datetime
    # posts: list[Post]
    # comments: list[Comment]
    # likes: list[Like]


class UserCreate(schemas.BaseUserCreate):
    username: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str]
