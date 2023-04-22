from _datetime import datetime, timedelta
from functools import wraps
from netschoolapi import errors, schemas

from app.sgo.constants import SYMBOLS, RESPONSES, DAY_FORMAT

from app.sgo import netschool


def exception_handler(method):
    """Обработчик ошибок, доставляет пользователю базовую информацию"""
    @wraps(method)
    async def wrapper(self, *method_args, **method_kwargs):
        try:
            result = await method(self, *method_args, **method_kwargs)
        except errors.NetSchoolAPIError:
            result = RESPONSES["netschool_error"]
        except Exception:
            result = RESPONSES["bot_error"]
        return result

    return wrapper


def assignment_transformer_homework(assignment):
    return assignment.content if assignment.type == "Домашнее задание" else ""


def lesson_transformer_homework(lesson: schemas.Lesson):
    assignments = list(filter(lambda x: len(x) > 0,
                              map(assignment_transformer_homework,
                                  lesson.assignments)))
    dz = '\nД/з: '
    return f"{lesson.number}.{lesson.subject}" \
           f"{dz if assignments else ''}{' '.join(assignments)}"


def get_period_report(schedule: list[schemas.Day]) -> dict:
    """Формирование словаря с отчетом за период"""
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


def form_period_report(schedule: list[schemas.Day],
                       show_average: bool) -> list[str]:
    """Формирование текста с отчетом за период"""
    data = get_period_report(schedule)
    result = []
    for subject, marks in data.items():
        result.append(f"{subject}: {''.join(SYMBOLS[mark] for mark in marks)}")
        # result.append(f"{subject}: {''.join(str(mark) for mark in marks)}")
        if show_average:
            # result[-1] += f"\nСредний балл: {round(sum(marks)/len(marks), 2)}"
            result[-1] += f"  Ср: {round(sum(marks) / len(marks), 2)}"
    return result


class NetschoolCollector:
    """Класс для текстовой обработки данных сетевого города"""

    def __init__(self):
        self.session = netschool.SGOProc()

    async def data_validator(self, lgdata) -> bool:
        """True для корректных данных, False для некорректных"""
        try:
            await self.session.empty_request(*lgdata)
            return True
        except Exception:
            return False

    @exception_handler
    async def school(self, lgdata):
        data = await self.session.get_school_data(*lgdata)
        return f"Название школы: {data.name}\n" \
               f"Директор: {data.director}\n" \
               f"Сайт: {data.site}\n" \
               f"Почта: {data.email}\n" \
               f"Контактный телефон: {data.phone}"

    @exception_handler
    async def homework(self, lgdata, time: datetime = datetime.now()):
        """Получение д/з на завтра"""
        data = await self.session.get_next_day(*lgdata, time)
        return f"Уроки на {datetime.strftime(data.day, DAY_FORMAT)}:" \
               f"\n" + \
            "\n".join(sorted(map(lesson_transformer_homework, data.lessons)))

    @exception_handler
    async def marks(self,
                    lgdata,
                    time: datetime = datetime.now(),
                    show_average: bool = False):
        """Получение оценок за ближайший день"""
        data = await self.session.get_last_day(*lgdata, time)
        result = form_period_report([data], show_average)
        if len(result) == 0:
            result.append(RESPONSES["no_homework"])
        return f"Результаты за {datetime.strftime(data.day, DAY_FORMAT)}:\n" \
            + "\n".join(result)

    @exception_handler
    async def period_marks(self, lgdata,
                           start_date: datetime = datetime.now() - timedelta(days=7),
                           end_date: datetime = datetime.now(),
                           show_average: bool = True):
        """Получение оценок за период"""
        data = await self.session.get_period(*lgdata, start_date, end_date)
        result = form_period_report(data, show_average)
        if len(result) == 0:
            result.append(RESPONSES["no_homework"])
        return f"Результаты за " \
               f"{datetime.strftime(start_date, DAY_FORMAT)}-" \
               f"{datetime.strftime(end_date, DAY_FORMAT)}:\n" + \
            '\n'.join(result)
