import datetime
from functools import wraps
from netschoolapi import NetSchoolAPI, errors, schemas

from constants import symbols

import netschool


# Обработчик ошибок, доставляет пользователю базовую информацию
def exception_handler(method):
    @wraps(method)
    async def wrapper(self, *method_args, **method_kwargs):
        # try:
        result = await method(self, *method_args, **method_kwargs)
        # except (errors.NetSchoolAPIError):
        #     result = "Ошибка Сетевого Города, попробуйте позже🙃"
        # except Exception:
        #     result = "Ошибка бота. Данные об ошибке получены, скоро исправим❤️‍🩹"
        return result
    return wrapper


def assignment_transformer_homework(assignment):
    return assignment.content if assignment.type == "Домашнее задание" else ""


def lesson_transformer_homework(lesson: schemas.Lesson):
    assignments = list(filter(lambda x: len(x) > 0,
                              map(assignment_transformer_homework, lesson.assignments)))
    dz = '\nД/з: '
    return f"{lesson.number}.{lesson.subject}{dz if len(assignments) > 0 else ''}{' '.join(assignments)}"


# Формирование словаря с отчетом за период
def get_period_report(schedule: list[schemas.Day]) -> dict:
    result = dict()
    for day in schedule:
        for lesson in day.lessons:
            lesson_marks = []
            for assignment in lesson.assignments:
                if assignment.mark is not None:
                    lesson_marks.append(assignment.mark)
                elif assignment.is_duty:
                    lesson_marks.append(0)
            if len(lesson_marks) > 0:
                result[lesson.subject] = result.get(
                    lesson.subject, []) + lesson_marks
    return result


# Формирование текста с отчетом за период
def form_period_report(schedule: list[schemas.Day], show_average: bool) -> list[str]:
    data = get_period_report(schedule)
    result = []
    for subject, marks in data.items():
        # result.append(f"{subject}: {''.join(symbols[mark] for mark in marks)}\nСредний балл: {sum(marks)/len(marks)}")
        result.append(
            f"{subject}: {''.join(str(mark) for mark in marks)}")
        if show_average:
            # result[-1] += f"\nСредний балл: {round(sum(marks)/len(marks), 2)}"
            result[-1] += f"  Ср: {round(sum(marks)/len(marks), 2)}"
    return result

# Класс для текстовой обработки данных сетевого города
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

    # Получение домашки на завтра
    @exception_handler
    async def homework(self, lgdata, time: datetime.datetime = datetime.datetime.now()):
        data = await self.session.get_next_day(*lgdata, time)
        return f"Уроки на {datetime.datetime.strftime(data.day, '%d.%m')}:" \
               f"\n" + \
            "\n".join(sorted(map(lesson_transformer_homework, data.lessons)))

    # Получение оценок за ближайший день
    @exception_handler
    async def marks(self, lgdata, time: datetime.datetime = datetime.datetime.now()):
        data = await self.session.get_last_day(*lgdata, time)
        result = form_period_report([data])
        if len(result) == 0:
            result.append("Нет оценок 👻")
        return f"Результаты за {datetime.datetime.strftime(data.day, '%d.%m')}:\n" + "\n".join(result)

    # Получение оценок за период
    @exception_handler
    async def period_marks(self, lgdata,
                           start_date: datetime.datetime = datetime.datetime.now(),
                           end_date: datetime.datetime = datetime.datetime.now(),
                           show_average: bool = True):
        data = await self.session.get_period(*lgdata, start_date, end_date)
        result = form_period_report(data, show_average)
        if len(result) == 0:
            result.append("Нет оценок 👻")
        return f"Результаты за {datetime.datetime.strftime(start_date, '%d.%m')}-{datetime.datetime.strftime(end_date, '%d.%m')}:\n" +\
            '\n'.join(result)
