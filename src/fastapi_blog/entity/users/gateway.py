from typing import Type, Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase, SQLAlchemyBaseOAuthAccountTable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_blog.entity.users.models import User


class UserGateway(SQLAlchemyUserDatabase):
    def __init__(
            self,
            session: AsyncSession,
            user_table: Type[User],
            oauth_account_table: Optional[Type[SQLAlchemyBaseOAuthAccountTable]] = None,
    ):
        super().__init__(session, user_table, oauth_account_table)

    async def last(self):
        stmt = (
            select(User.id).
            order_by(User.id.desc())
        )
        last_id = await self.session.scalar(stmt)
        return await self.get(last_id)

