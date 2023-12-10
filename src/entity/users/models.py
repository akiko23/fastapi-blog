from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import TablenameMixin, TimestampColumnsMixin

if TYPE_CHECKING:
    from src.entity.comments.models import Comment
    from src.entity.likes.models import Like
    from src.entity.posts.models import Post

MAX_NICKNAME_LENGTH = 64
MAX_EMAIL_LENGTH = 128


class User(Base, TablenameMixin, TimestampColumnsMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(
        String(MAX_NICKNAME_LENGTH), default="pidoras"
    )
    email: Mapped[str] = mapped_column(String(MAX_EMAIL_LENGTH))
    password: Mapped[str] = mapped_column()

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
