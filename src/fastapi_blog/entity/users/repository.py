from typing import Optional, Type

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseOAuthAccountTable,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_blog.entity.users.models import User


class UserRepository(SQLAlchemyUserDatabase[User, int]):
    def __init__(
        self,
        session: AsyncSession,
        user_table: Type[User],
        oauth_account_table: Optional[
            Type[SQLAlchemyBaseOAuthAccountTable[int]]
        ] = None,
    ) -> None:
        super().__init__(session, user_table, oauth_account_table)

    async def last(self) -> Optional[User]:
        stmt = select(User.id).order_by(User.id.desc())
        last_id = await self.session.scalar(stmt)
        if last_id is None:
            return None
        return await self.get(last_id)
