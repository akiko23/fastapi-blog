from typing import Optional, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import TablenameMixin

if TYPE_CHECKING:
    from src.posts.models import Post
    from src.comments.models import Comment
    from src.likes.models import Like


class User(Base, TablenameMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64))
    surname: Mapped[str] = mapped_column(String(64))
    patronamyc: Mapped[Optional[str]] = mapped_column(String(64))

    # relationships
    posts: Mapped[list['Post']] = relationship(back_populates='user', cascade='all, delete')
    comments: Mapped[list['Comment']] = relationship(back_populates='user', cascade='all, delete')
    likes: Mapped[list['Like']] = relationship(back_populates='user', cascade='all, delete')

