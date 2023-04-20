from pprint import pprint
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.dao.holder import HolderDao
from app.models import dto
from app.services.chat import upsert_chat
from app.services.user import upsert_user
from app.services.SGOUser import upsert_sgo_user
from app.handlers.base import SGORegistrate


class LoadDataMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]) -> Any:
        holder_dao = data["dao"]
        data["user"] = await save_user(data, holder_dao)
        data["chat"] = await save_chat(data, holder_dao)
        if await data['state'].get_state() == SGORegistrate.save_to_db:
            data['sgo'] = await save_sgo_user(data, holder_dao)
        return await handler(event, data)


async def save_user(data: dict[str, Any], holder_dao: HolderDao) -> dto.User:
    return await upsert_user(
        dto.User.from_aiogram(data["event_from_user"]),
        holder_dao.user
    )


async def save_chat(data: dict[str, Any], holder_dao: HolderDao) -> dto.Chat:
    return await upsert_chat(
        dto.Chat.from_aiogram(data["event_chat"]),
        holder_dao.chat
    )


async def save_sgo_user(data: dict[str, Any], holder_dao: HolderDao) -> dto.SGOUser:
    return await upsert_sgo_user(
        dto.SGOUser.from_aiogram(await data['state'].get_data()), holder_dao.sgo)
