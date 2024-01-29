from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_blog.database.base import Base
from fastapi_blog.database.mixins import TablenameMixin
from fastapi_blog.entity.comments.models import Comment
from fastapi_blog.entity.likes.models import Like
from fastapi_blog.entity.posts.models import Post

MAX_NICKNAME_LENGTH = 64


class User(Base, TablenameMixin, SQLAlchemyBaseUserTable):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(MAX_NICKNAME_LENGTH), unique=True
    )
    registered_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # relationships
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    likes: Mapped[list["Like"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
