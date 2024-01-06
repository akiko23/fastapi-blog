from datetime import datetime
from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser):
    username: str
    registered_at: datetime
    # posts: list[Post]
    # comments: list[Comment]
    # likes: list[Like]


class UserCreate(schemas.BaseUserCreate):
    username: Optional[str]


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str]
