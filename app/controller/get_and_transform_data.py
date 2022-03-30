from datetime import datetime, time, date

from flask_login import current_user

from app.config import db
from app.model import *


def analyze_week(week_number):
    """
    По номеру недели рассчитывает ее длину в днях, количество записей, суммарную эффективность за все дни недели,
    суммарное время сна за все дни недели.
    """
    sum_of_minutes, sum_of_efficiency, week_length, amount = 0, 0, 0, 0
    first_day_of_week = 7 * (week_number - 1) + 1
    last_day_of_week = 8 * week_number - (week_number - 1)
    all_notations = db.session.query(Notation).order_by(Notation.calendar_date).filter_by(user_id=current_user.id)
    for day in range(first_day_of_week, last_day_of_week):
        for day_number, _notation in enumerate(all_notations, start=1):
            if day_number != day:
                continue
            week_length += 1
            amount += 1
            sum_of_minutes += _notation.sleep_duration
            if _notation.sleep_duration != 0:
                sum_of_efficiency += _notation.sleep_duration / _notation.time_in_bed
    return week_length, amount, sum_of_efficiency, sum_of_minutes


def get_average_sleep_efficiency_per_week(week_number):
    """Вычисляет среднюю эффективность сна за неделю"""
    week_length, sum_of_efficiency = analyze_week(week_number)[0], analyze_week(week_number)[2]
    if week_length == 0:
        return 0
    return round(((sum_of_efficiency / week_length) * 100), 2)


def get_average_sleep_duration_per_week(week_number):
    """Вычисляет среднюю продолжительность сна за неделю"""
    week_length, sum_of_minutes = analyze_week(week_number)[0], analyze_week(week_number)[3]
    if week_length == 0:
        return 0
    return int(sum_of_minutes / week_length)


def get_amount_notations_of_week(week_number):
    """Рассчитывает количество добавленных записей в неделе"""
    amount = analyze_week(week_number)[1]
    if amount == 0:
        return 0
    return amount


def today_date():
    """Возвращает текущую локальную дату в формате 'YYYY-MM-DD'"""
    return datetime.date(datetime.today())


def str_to_time(string_time: str):
    """Изменяет тип данных str на time в формате 'HH:MM'"""
    return datetime.time(datetime.strptime(string_time, '%H:%M'))


def str_to_date(string_date: str):
    """Изменяет тип данных str на date в формате 'YYYY-MM-DD'"""
    return datetime.date(datetime.strptime(string_date, '%Y-%m-%d'))


def sleep_efficiency(sleep_duration: int, time_in_bed: int):
    """Вычисляет эффективность сна(отношение времени сна к времени нахождения в кровати) в процентах"""
    if sleep_duration == 0:
        return 0
    return round((sleep_duration / time_in_bed) * 100, 2)


def date_and_time_display(date_and_time: datetime):
    """Отображает время из базы данных в более дружелюбное для пользователя"""
    return date_and_time.strftime('%Y-%m-%d %H:%M')


def time_display(time_point: int or time):
    """Конвертирует время из типа данных int или time в str в формате 'HH:MM'"""
    if isinstance(time_point, int):
        if time_point % 60 < 10:
            return str(time_point // 60) + ':0' + str(time_point % 60)
        return str(time_point // 60) + ':' + str(time_point % 60)
    elif isinstance(time_point, time):
        return time_point.strftime('%H:%M')
    else:
        raise TypeError


def get_timedelta(calendar_date: date, time_point_1: time, time_point_2: time):
    """Получает временной интервал между двумя точками, каждая из которых скомбинирована из даты с времени"""
    return datetime.combine(calendar_date, time_point_1) - datetime.combine(calendar_date, time_point_2)
