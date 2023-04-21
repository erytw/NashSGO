from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.models.db import SGOUser
from app.models import dto


class SGOUserDAO(BaseDAO[SGOUser]):
    def __init__(self, session: AsyncSession):
        super().__init__(SGOUser, session)

    async def get_by_tg_id(self, tg_id: int) -> dto.SGOUser:
        result = await self.session.execute(
            select(SGOUser).where(SGOUser.tg_id == tg_id)
        )
        return result.scalar_one().to_dto()

    async def upsert_user(self, user: dto.SGOUser) -> dto.SGOUser:
        kwargs = dict(
            tg_id=user.tg_id,
            login=user.login,
            password=user.password,
            school=user.school,
        )
        saved_user = await self.session.execute(
            insert(SGOUser)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(SGOUser.tg_id,),
                set_=kwargs,
                where=SGOUser.tg_id == user.tg_id
            )
            .returning(SGOUser)
        )
        return saved_user.scalar_one().to_dto()
