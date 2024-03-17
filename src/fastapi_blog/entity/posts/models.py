from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_blog.database.base import Base
from fastapi_blog.database.mixins import TablenameMixin, TimestampColumnsMixin

if TYPE_CHECKING:
    from fastapi_blog.entity.comments.models import Comment
    from fastapi_blog.entity.likes.models import Like
    from fastapi_blog.entity.users.models import User

MAX_POST_TITLE_LENGTH = 128
MAX_POST_TEXT_LENGTH = 4096


class Post(Base, TablenameMixin, TimestampColumnsMixin):  # type: ignore[misc]
    """Represent table 'posts' in database."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(MAX_POST_TITLE_LENGTH))
    content: Mapped[str] = mapped_column(String(MAX_POST_TEXT_LENGTH))

    # foreign keys and relationships
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    # relationships
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="post", cascade="all, delete"
    )
    likes: Mapped[List["Like"]] = relationship(
        back_populates="post", cascade="all, delete"
    )
