from datetime import datetime, time, date, timedelta
from typing import Optional, Union

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.controller import *
from app.model import *

# self.calendar_date = datetime.strptime(request.form['calendar_date'], "%Y-%m-%d")
# self._bedtime = str_to_time(request.form['bedtime'][:5])
# self._asleep = str_to_time(request.form['asleep'][:5])
# self._awake = str_to_time(request.form['awake'][:5])
# self._rise = str_to_time(request.form['rise'][:5])
# self._without_sleep = str_to_time(request.form['without_sleep'][:5])


# without_sleep = without_sleep.hour * 60 + without_sleep.minute
# sleep_duration = get_timedelta(calendar_date, awake, asleep).seconds / 60 - without_sleep
# time_in_bed = get_timedelta(calendar_date, rise, bedtime).seconds / 60


class DiaryEntryManager:
    def __init__(self, calendar_date: Optional[Union[str, date]], bedtime=None, asleep=None, awake=None, rise=None,
                 without_sleep=None):
        self.__calendar_date = calendar_date
        self.__bedtime = bedtime
        self.__asleep = asleep
        self.__awake = awake
        self.__rise = rise
        self.__without_sleep = without_sleep
        if isinstance(self.__calendar_date, date) and isinstance(self.__bedtime, time):
            self.__correct_sleep_time(self.__calendar_date, self.__bedtime, self.__asleep)
            self.__correct_wake_up_time(self.__calendar_date, self.__awake, self.__rise)
            self.__correct_durations(self.__calendar_date, self.__bedtime, self.__asleep, self.__awake, self.__rise)
        # else:
            # self._sleep_duration = sleep_duration
            # self._time_in_bed = time_in_bed

    def __repr__(self):
        return f"\n\nЗаготовка для записи: [Дата: {self.__calendar_date}, Лег: {self.__bedtime}, Уснул: " \
               f"{self.__asleep}, Проснулся: {self.__awake}, Встал: {self.__rise}, Не спал: {self.__without_sleep}]\n\n"

    @classmethod
    def __correct_sleep_time(cls, calendar_date, bedtime, asleep):
        if bedtime > asleep:
            datetime_bedtime = datetime.combine(calendar_date, bedtime)
            datetime_asleep = datetime.combine(
                date(calendar_date.year, calendar_date.month, calendar_date.day + 1),
                asleep
            )
            if bedtime.hour == asleep.hour and bedtime.minute > asleep.minute:
                """Вызывает ошибку если уснул раньше чем лег в рамках часа"""
                raise ValueError("Не можешь в рамках часа уснуть раньше чем лег!")
            elif datetime_asleep - datetime_bedtime > timedelta(hours=12):
                """Вызывает ошибку если разница между отходом ко сну и засыпанием больше 12 часов"""
                raise ValueError("Время отхода ко сну не может быть позже времени засыпания!\n"
                                 "Или время между этими событиями не может быть более 12 часов!")

    @classmethod
    def __correct_wake_up_time(cls, calendar_date, awake, rise):
        if awake > rise:
            datetime_awake = datetime.combine(calendar_date, awake)
            datetime_rise = datetime.combine(date(calendar_date.year, calendar_date.month, calendar_date.day + 1), rise)
            if awake.hour == rise.hour and awake.minute > rise.minute:
                """"""
                raise ValueError("Не можешь в рамках часа уснуть раньше чем лег!")
            elif datetime_rise - datetime_awake > timedelta(hours=12):
                """"""
                raise ValueError("Время пробуждения не может быть позже времени подъема с кровати!\n"
                                 "Или время между этими событиями не может быть более 12 часов!")

    @classmethod
    def __correct_durations(cls, calendar_date, bedtime, asleep, awake, rise):
        sleep_duration = get_timedelta(calendar_date, awake, asleep).seconds / 60
        time_in_bed = get_timedelta(calendar_date, rise, bedtime).seconds / 60
        if time_in_bed < sleep_duration:
            raise ValueError('Время проведенное в кровати не может быть меньше времени сна.')

    @staticmethod
    def get_data_forms():
        calendar_date = datetime.strptime(request.form['calendar_date'], "%Y-%m-%d")
        bedtime = str_to_time(request.form['bedtime'][:5])
        asleep = str_to_time(request.form['asleep'][:5])
        awake = str_to_time(request.form['awake'][:5])
        rise = str_to_time(request.form['rise'][:5])
        without_sleep = str_to_time(request.form['without_sleep'][:5])
        return DiaryEntryManager(calendar_date, bedtime, asleep, awake, rise, without_sleep)

    # todo добавить подсчет времени сна и времени в кровати
    @staticmethod
    def get_entry_from_db(notations: list[Notation]):
        list_of_instances = []
        for notation in notations:
            calendar_date = f"{notation.calendar_date:'%d-%m-%Y'}"
            bedtime = f"{notation.bedtime:'%H:%M'}"
            asleep = f"{notation.asleep:'%H:%M'}"
            awake = f"{notation.awake:'%H:%M'}"
            rise = f"{notation.rise:'%H:%M'}"
            without_sleep = f"{notation.without_sleep:'%H:%M'}"
            list_of_instances.append(DiaryEntryManager(calendar_date, bedtime, asleep, awake, rise, without_sleep))
        return list_of_instances

    @property
    def calendar_date(self):
        return self.__calendar_date

    @property
    def bedtime(self):
        return self.__bedtime

    @property
    def asleep(self):
        return self.__asleep

    @property
    def awake(self):
        return self.__awake

    @property
    def rise(self):
        return self.__rise

    @property
    def without_sleep(self):
        return self.__without_sleep


