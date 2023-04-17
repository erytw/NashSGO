import datetime
from functools import wraps
from netschoolapi import NetSchoolAPI, errors, schemas

# from constants import symbols

import netschool


def exception_handler(method):
    @wraps(method)
    async def wrapper(self, *method_args, **method_kwargs):
        try:
            result = await method(self, *method_args, **method_kwargs)
        except Exception:
            result = "Ошибка Сетевого Города, попробуйте позже"
        return result
    return wrapper


def assignment_transformer_homework(assignment):
    return assignment.content if assignment.type == "Домашнее задание" else ""


def lesson_transformer_homework(lesson: schemas.Lesson):
    assignments = list(filter(lambda x: len(x) > 0,
                              map(assignment_transformer_homework, lesson.assignments)))
    dz = '\nД/з: '
    return f"{lesson.number}.{lesson.subject}{dz if len(assignments) > 0 else ''}{' '.join(assignments)}"


class netschool_collector():
    def __init__(self):
        self.session = netschool.sgoproc()

    @exception_handler
    async def school(self, lgdata):
        data = await self.session.get_school_data(*lgdata)
        return f"Название школы: {data.name}\n" \
               f"Директор: {data.director}\n" \
               f"Сайт: {data.site}\n" \
               f"email: {data.email}\n" \
               f"Контактный телефон: {data.phone}"

    @exception_handler
    async def homework(self, lgdata):
        data = await self.session.get_next_day(*lgdata)
        return f"Уроки на {datetime.datetime.strftime(data.day, '%d.%m')}:" \
               f"\n"+"\n".join(sorted(map(lesson_transformer_homework, data.lessons)))
