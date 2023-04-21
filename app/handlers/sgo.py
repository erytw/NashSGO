import logging

from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.dao.holder import HolderDao
from app.sgo.data_wrapper import NetschoolCollector
from app.services.SGOUser import get_sgo_user

logger = logging.getLogger(__name__)
collector = NetschoolCollector()


class SGORegistrate(StatesGroup):
    choosing_login = State()
    choosing_password = State()
    choosing_school = State()
    save_to_db = State()


async def login_cmd(message: Message, state: FSMContext):
    await message.answer(text="Пришлите ваш логин:")
    await state.set_state(SGORegistrate.choosing_login)


async def login(message: Message, state: FSMContext):
    await state.update_data(tg_id=message.from_user.id)
    await state.update_data(login=message.text)
    await message.answer(text="Пришлите ваш пароль:")
    await state.set_state(SGORegistrate.choosing_password)


async def password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer(text="Пришлите школу:")
    await state.set_state(SGORegistrate.choosing_school)


async def school(message: Message, state: FSMContext):
    await state.update_data(school=message.text)
    data = await state.get_data()
    print(data)
    if await collector.data_validator((data['login'],
                                       data['password'],
                                       data['school'])):
        await state.set_state(SGORegistrate.save_to_db)
    else:
        await message.answer('Данные некорректны, попробуйте снова')
        await message.answer('Введите логин:')
        await state.set_state(SGORegistrate.choosing_login)


async def approve_data_sgo(message: Message, state: FSMContext):
    await message.answer(text="Аккаунт Добавлен")
    await state.clear()


async def continue_reg_sgo(message: Message, state: FSMContext):
    pass


async def school_info(message: Message, dao: HolderDao):
    user = await get_sgo_user(message.from_user.id, dao.sgo)
    ans = await collector.school(user.to_sgo)
    await message.answer(ans)


def setup_sgo(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(login_cmd, Command('login'))
    router.message.register(school_info, Command('school'))
    router.message.register(login, SGORegistrate.choosing_login)
    router.message.register(password, SGORegistrate.choosing_password)
    router.message.register(school, SGORegistrate.choosing_school)
    router.message.register(approve_data_sgo, SGORegistrate.save_to_db)

    dp.include_router(router)
