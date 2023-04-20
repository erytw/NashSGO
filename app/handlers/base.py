import logging

from aiogram import Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, ContentType

from aiogram.utils.markdown import html_decoration as hd

from app.dao.holder import HolderDao
from app.models import dto
from app.services.chat import update_chat_id

logger = logging.getLogger(__name__)


class SGORegistrate(StatesGroup):
    choosing_login = State()
    choosing_password = State()
    choosing_school = State()


async def start_cmd(message: Message):
    await message.reply("Hi!")


async def login_cmd(message: Message, state: FSMContext):
    await message.answer(text="Пришлите ваш логин:")
    await state.set_state(SGORegistrate.choosing_login)


async def login(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer(text="Пришлите ваш пароль:")
    await state.set_state(SGORegistrate.choosing_password)


async def password(message: Message, state: FSMContext):
    await state.update_data(passsword=message.text.lower())
    await message.answer(text="Пришлите школу:")
    await state.set_state(SGORegistrate.choosing_school)
    

async def end_logining(message: Message, state: FSMContext):
    await state.update_data(school=message.text.lower())
    data = await state.get_data()
    await message.answer(text="Данные верны")
    print(data)
    await state.clear()


async def chat_id(message: Message):
    text = (
        f"chat_id: {hd.pre(message.chat.id)}\n"
        f"your user_id: {hd.pre(message.from_user.id)}"
    )
    if message.reply_to_message:
        text += (
            f"\nid {hd.bold(message.reply_to_message.from_user.full_name)}: "
            f"{hd.pre(message.reply_to_message.from_user.id)}"
        )
    await message.reply(text, disable_notification=True)


async def cancel_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logger.info('Cancelling state %s', current_state)
    # Cancel state and inform user about it
    await state.clear()
    # And remove keyboard (just in case)
    await message.reply('Dialog stopped, data removed', reply_markup=ReplyKeyboardRemove())


async def chat_migrate(message: Message, chat: dto.Chat, dao: HolderDao):
    new_id = message.migrate_to_chat_id
    await update_chat_id(chat, new_id, dao.chat)
    logger.info("Migrate chat from %s to %s", message.chat.id, new_id)


def setup_base(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(start_cmd, Command("start"))
    router.message.register(login_cmd, Command('login'))
    router.message.register(login, SGORegistrate.choosing_login)
    router.message.register(password, SGORegistrate.choosing_password)
    router.message.register(end_logining, SGORegistrate.choosing_school)
    router.message.register(
        chat_id, Command(commands=["idchat", "chat_id", "id"], prefix="/!"),
    )
    router.message.register(cancel_state, Command(commands="cancel"))
    router.message.register(
        chat_migrate, F.content_types == ContentType.MIGRATE_TO_CHAT_ID,
    )
    dp.include_router(router)
