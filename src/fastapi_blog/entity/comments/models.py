from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_blog.database.base import Base
from fastapi_blog.database.mixins import TablenameMixin, TimestampColumnsMixin

if TYPE_CHECKING:
    from fastapi_blog.entity.likes.models import Like
    from fastapi_blog.entity.posts.models import Post
    from fastapi_blog.entity.users.models import User

MAX_COMMENT_LENGTH = 4096


class Comment(Base, TablenameMixin, TimestampColumnsMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(MAX_COMMENT_LENGTH))

    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))

    # Relationships
    user: Mapped["User"] = relationship(
        back_populates="comments", foreign_keys=[user_id]
    )
    post: Mapped["Post"] = relationship(
        back_populates="comments", foreign_keys=[post_id]
    )
    likes: Mapped[list["Like"]] = relationship(
        back_populates="comment", cascade="all, delete"
    )
