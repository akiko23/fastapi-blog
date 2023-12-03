from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import declared_attr, Mapped, mapped_column


class TablenameMixin:
    """Add the __tablename__ attribute as the plural name of the model."""

    @declared_attr
    def __tablename__(cls):  # noqa
        return cls.__name__.lower() + 's'


class TimestampColumnsMixin:
    """Add `created_on` and `updated_on` columns to the model."""

    created_on: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_on: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=datetime.now)
