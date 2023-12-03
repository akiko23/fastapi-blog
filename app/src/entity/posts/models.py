from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.mixins import TablenameMixin

if TYPE_CHECKING:
    from src.users.models import User
    from src.comments.models import Comment
    from src.likes.models import Like


class Post(Base, TablenameMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str]

    # foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    # relationships
    user: Mapped['User'] = relationship(back_populates='posts')
    comments: Mapped[list['Comment']] = relationship(back_populates='post', cascade='all, delete')
    likes: Mapped[list['Like']] = relationship(back_populates='post', cascade='all, delete')

