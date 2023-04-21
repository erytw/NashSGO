from app.dao import SGOUserDAO
from app.models import dto


async def upsert_sgo_user(user: dto.SGOUser, dao: SGOUserDAO) -> dto.SGOUser:
    saved_user = await dao.upsert_user(user)
    await dao.commit()
    return saved_user


async def get_sgo_user(tg_id: int, dao: SGOUserDAO) -> dto.SGOUser:
    sgo_user = await dao.get_by_tg_id(tg_id)
    return sgo_user
