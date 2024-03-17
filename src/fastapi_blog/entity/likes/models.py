from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_blog.database.base import Base
from fastapi_blog.database.mixins import TablenameMixin, TimestampColumnsMixin

if TYPE_CHECKING:
    from fastapi_blog.entity.comments.models import Comment
    from fastapi_blog.entity.posts.models import Post
    from fastapi_blog.entity.users.models import User


class Like(Base, TablenameMixin, TimestampColumnsMixin):  # type: ignore[misc]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE")
    )
    comment_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE")
    )

    # relationships
    user: Mapped["User"] = relationship(back_populates="likes", foreign_keys=[user_id])
    post: Mapped[Optional["Post"]] = relationship(
        back_populates="likes", foreign_keys=[post_id]
    )
    comment: Mapped[Optional["Comment"]] = relationship(
        back_populates="likes", foreign_keys=[comment_id]
    )
