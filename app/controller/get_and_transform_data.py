from datetime import datetime, time, date, timedelta
from typing import Union


def today_date() -> date:
    """Возвращает текущую дату в формате 'YYYY-MM-DD'"""
    return datetime.date(datetime.today())


def str_to_date(string_date):
    """Изменяет тип данных str на date в формате 'YYYY-MM-DD'"""
    return datetime.date(datetime.strptime(string_date, "%Y-%m-%d"))


def str_to_time(string_time: str) -> time:
    """Изменяет тип данных str на time в формате 'HH:MM'"""
    return datetime.time(datetime.strptime(string_time, '%H:%M'))


def date_and_time_display(date_and_time: datetime) -> str:
    """Конвертирует время из бд из datetime в str"""
    return date_and_time.strftime('%Y-%m-%d %H:%M')


def time_display(time_point: Union[int, float, time]) -> str:
    """Конвертирует время из типа данных int или time в str в формате 'HH:MM'"""
    if isinstance(time_point, int) or isinstance(time_point, float):
        time_point = int(time_point)
        if time_point == 0:
            return '00:00'
        elif time_point % 60 < 10:
            return f"{time_point // 60}:0{time_point % 60}"
        return f"{time_point // 60}:{time_point % 60}"
    elif isinstance(time_point, time):
        return f"{time_point:%H:%M}"
    else:
        raise TypeError('Ошибка типа данных времени.')


def get_timedelta(calendar_date: date, time_point_1: time, time_point_2: time) -> timedelta:
    """Получает временной интервал между двумя точками, каждая из которых скомбинирована из даты с времени"""
    return datetime.combine(calendar_date, time_point_1) - datetime.combine(calendar_date, time_point_2)
