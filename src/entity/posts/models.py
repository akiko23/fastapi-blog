from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import TablenameMixin, TimestampColumnsMixin

if TYPE_CHECKING:
    from src.entity.comments.models import Comment
    from src.entity.likes.models import Like
    from src.entity.users.models import User

MAX_POST_TITLE_LENGTH = 128
MAX_POST_TEXT_LENGTH = 4096


class Post(Base, TablenameMixin, TimestampColumnsMixin):
    """Represent table 'posts' in database."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(MAX_POST_TITLE_LENGTH))
    content: Mapped[str] = mapped_column(String(MAX_POST_TEXT_LENGTH))

    # foreign keys and relationships
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    # relationships
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="post", cascade="all, delete"
    )
    likes: Mapped[list["Like"]] = relationship(
        back_populates="post", cascade="all, delete"
    )
