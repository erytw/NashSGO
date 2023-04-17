import asyncio
import datetime
from netschoolapi import NetSchoolAPI
from functools import wraps

# Декоратор для авторизации пользователя при запросах


def login(method):
    @wraps(method)
    async def wrapper(self, login: str, password: str, school: str | int, *method_args, **method_kwargs):
        await self.ns.login(login, password, school)
        result = await method(self, *method_args, **method_kwargs)
        await self.ns.logout()
        return result
    return wrapper


# Класс для взаимодействия с библиотекой
class sgoproc():
    def __init__(self, host: str = 'https://edu.admoblkaluga.ru:444/'):
        self.ns = NetSchoolAPI(host)

    # Получение информации о школе
    @login
    async def get_school_data(self):
        return await self.ns.school()

    # Получение дневника без фишек
    @login
    async def get_diary_data(self, _start=None, _end=None):
        if _end is None:
            _end = _start
        return await self.ns.diary(start=_start, end=_end)

    # Получение ближайшего дня с уроками
    @login
    async def get_next_day(self, date=datetime.datetime.now()):
        # Если время>=16:00, то перелистнем на следующий день, смотрим расписание на завтра
        date += datetime.timedelta(hours=8)
        date = date.date()
        return (await self.ns.diary(start=date, end=date+datetime.timedelta(days=7))).schedule[0]

    # Получение ближайшего прошедшего дня
    @login
    async def get_last_day(self, date=datetime.datetime.now()):
        # До 8 часов утра смотрим на предыдущий день
        date -= datetime.timedelta(hours=8)
        date = date.date()
        return (await self.ns.diary(start=date-datetime.timedelta(days=7), end=date)).schedule[-1]
