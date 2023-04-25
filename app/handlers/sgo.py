import logging
from app.services.SGOUser import get_sgo_user
from app.sgo.data_wrapper import NetschoolCollector
from app.dao.holder import HolderDao
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Text
from aiogram import Dispatcher, Router
import app.handlers.keyboards as kb


logger = logging.getLogger(__name__)
collector = NetschoolCollector()


class SGOInterface(StatesGroup):
    registration = State()
    choosing_login = State()
    choosing_password = State()
    choosing_school = State()
    save_to_db = State()
    main_menu = State()


async def registration(message: Message, state: FSMContext):
    await message.answer(text="Выберите школу:\n(`МБОУ \"Средняя общеобразовательная школа № x\" г. Калуги`)", reply_markup=kb.remove)
    await state.set_state(SGOInterface.choosing_school)


async def school(message: Message, state: FSMContext):
    await state.update_data(school=message.text)
    await message.answer(text="Пришлите ваш логин:")
    await state.set_state(SGOInterface.choosing_login)


async def login(message: Message, state: FSMContext):
    await state.update_data(tg_id=message.from_user.id)
    await state.update_data(login=message.text)
    await message.answer(text="Пришлите ваш пароль:")
    await state.set_state(SGOInterface.choosing_password)


async def password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    if await collector.data_validator((data['login'], data['password'], data['school'])):
        await message.answer(text="Аккаунт Добавлен🤩", reply_markup=kb.call_main_menu)
        await state.set_state(SGOInterface.save_to_db)
        # await state.set_state(SGOInterface.main_menu)
    else:
        await message.answer('Данные некорректны, пожалуйста, попробуйте снова.', reply_markup=kb.register)
        await state.clear()


async def approve_data_sgo(message: Message, state: FSMContext):
    await message.answer("Главное меню:", reply_markup=kb.main_menu)
    await state.set_state(SGOInterface.main_menu)


async def call_main_menu(message: Message, state: FSMContext):
    await message.answer("Главное меню:", reply_markup=kb.main_menu)
    await state.set_state(SGOInterface.main_menu)


async def main_menu(message: Message, state: FSMContext, dao: HolderDao):
    data = await get_sgo_user(message.from_user.id, dao.sgo)
    if message.text == "Ближайшее Д/з":
        await message.answer(await collector.homework(data.to_sgo))
    elif message.text == "Оценки за день":
        await message.answer(await collector.marks(data.to_sgo))
    elif message.text == "Оценки за 7 дней":
        await message.answer(await collector.period_marks(data.to_sgo))
    elif message.text == "Данные школы":
        await message.answer(await collector.school(data.to_sgo))
    elif message.text == "Перерегистрация":
        await message.answer(text="Выберите школу:", reply_markup=kb.remove)
        await state.set_state(SGOInterface.choosing_school)


def setup_sgo(dp: Dispatcher):
    router = Router(name=__name__)
    router.message.register(registration, Command('register'))
    router.message.register(registration, Text('Регистрация'))
    router.message.register(registration, SGOInterface.registration)
    router.message.register(school, SGOInterface.choosing_school)
    router.message.register(login, SGOInterface.choosing_login)
    router.message.register(password, SGOInterface.choosing_password)
    router.message.register(approve_data_sgo, SGOInterface.save_to_db)
    router.message.register(main_menu, SGOInterface.main_menu)
    router.message.register(call_main_menu, Command('menu'))
    router.message.register(call_main_menu, Text("Меню"))

    dp.include_router(router)
