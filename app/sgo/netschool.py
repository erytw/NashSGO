from datetime import datetime, timedelta
from functools import wraps

from netschoolapi import NetSchoolAPI

from app.sgo.constants import HOST


def login(method):
    """Декоратор для авторизации пользователя при запросах"""
    @wraps(method)
    async def wrapper(self,
                      login: str,
                      password: str,
                      school: str | int,
                      *method_args,
                      **method_kwargs):
        await self.ns.login(login, password, school)
        result = await method(self, *method_args, **method_kwargs)
        await self.ns.logout()
        return result
    return wrapper


class SGOProc:
    """Класс для взаимодействия с библиотекой"""

    def __init__(self, host: str = HOST):
        self.ns = NetSchoolAPI(host)

    @login
    async def empty_request(self):
        """Пустой запрос для сверки данных"""
        return

    @login
    async def get_school_data(self):
        """Получение информации о школе"""
        return await self.ns.school()

    @login
    async def get_diary_data(self, _start=None, _end=None):
        """Получение дневника без фишек"""
        if _end is None:
            _end = _start
        return await self.ns.diary(start=_start,
                                   end=_end)

    @login
    async def get_next_day(self, date=datetime.now()):
        """Получение ближайшего дня с уроками"""
        # Если время >= 16:00, то смотрим расписание на завтра
        date += timedelta(hours=8)
        date = date.date()
        return (await self.ns.diary(start=date,
                                    end=date+timedelta(days=7))).schedule[0]

    @login
    async def get_last_day(self, date=datetime.now()):
        """Получение ближайшего прошедшего дня"""
        # До 8 часов утра смотрим на предыдущий день
        date -= timedelta(hours=8)
        date = date.date()
        return (await self.ns.diary(start=date-timedelta(days=7),
                                    end=date)).schedule[-1]

    @login
    async def get_period(self,
                         start_date: datetime = datetime.now(),
                         end_date: datetime = datetime.now()):
        """Получение периода (Для отчетов)"""
        start_date = start_date.date()
        end_date = end_date.date()
        return (await self.ns.diary(start=start_date, end=end_date)).schedule
