from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import TablenameMixin, TimestampColumnsMixin

if TYPE_CHECKING:
    from src.entity.posts.models import Post
    from src.entity.likes.models import Like
    from src.entity.users.models import User

MAX_COMMENT_LENGTH = 4096


class Comment(Base, TablenameMixin, TimestampColumnsMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(MAX_COMMENT_LENGTH))

    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete='CASCADE'))

    # Relationships
    user: Mapped['User'] = relationship(back_populates='comments', foreign_keys=[user_id])
    post: Mapped['Post'] = relationship(back_populates='comments', foreign_keys=[post_id])
    likes: Mapped[list['Like']] = relationship(back_populates='comment', cascade='all, delete')
