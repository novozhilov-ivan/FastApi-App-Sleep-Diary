from datetime import datetime, time, date, timedelta
from typing import Optional, Union

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.controller import *
from app.model import *

# todo по аналогии с временем сна добавить подсчет времени в кровати и эффективности сна за ночь
# todo Добавить метод который возвращает список со средними значениями за неделю


# without_sleep = without_sleep.hour * 60 + without_sleep.minute
# sleep_duration = get_timedelta(calendar_date, awake, asleep).seconds / 60 - without_sleep
# time_in_bed = get_timedelta(calendar_date, rise, bedtime).seconds / 60

TIME_FORMAT = '%H:%M'


class DiaryEntryManager:
    def __repr__(self):
        return f"\n\nЗаготовка для записи: [Дата: {self.__calendar_date}, Лег: {self.__bedtime}, Уснул: " \
               f"{self.__asleep}, Проснулся: {self.__awake}, Встал: {self.__rise}, Не спал: {self.__without_sleep}]\n\n"

    def __init__(self, calendar_date=None, bedtime=None, asleep=None, awake=None, rise=None, without_sleep=None,
                 sleep_duration=None):
        self.calendar_date = calendar_date
        self.bedtime = bedtime
        self.asleep = asleep
        self.awake = awake
        self.rise = rise
        self.without_sleep = without_sleep
        self.__sleep_duration = sleep_duration
        self.__check_timings()

    def get_sleep_duration(self):
        without_sleep = self.__without_sleep.hour * 60 + self.__without_sleep.minute
        sleep_timing = int(
            (
                    datetime.combine(self.__calendar_date, self.__awake) -
                    datetime.combine(self.__calendar_date, self.__asleep)
            ).seconds / 60
        )
        return time_display(sleep_timing - without_sleep)

    def __check_timings(self):
        if (self.__calendar_date or self.__bedtime or self.__asleep or self.__awake or self.__rise) is None:
            return

        if self.__awake > self.__rise:
            datetime_awake = datetime.combine(self.__calendar_date, self.__awake)
            datetime_rise = datetime.combine(
                date(self.__calendar_date.year, self.__calendar_date.month, self.__calendar_date.day + 1),
                self.__rise
            )
            if self.__awake.hour == self.__rise.hour and self.__awake.minute > self.__rise.minute:
                raise ValueError("Не можешь в рамках часа проснуться позже чем встал с кровати!")
            elif datetime_rise - datetime_awake > timedelta(hours=12):
                raise ValueError("Время пробуждения не может быть позже времени подъема с кровати!\n"
                                 "Или время между этими событиями не может быть более 12 часов!")

        if self.__bedtime > self.__asleep:
            datetime_bedtime = datetime.combine(self.__calendar_date, self.__bedtime)
            datetime_asleep = datetime.combine(
                date(self.__calendar_date.year, self.__calendar_date.month, self.__calendar_date.day + 1),
                self.__asleep
            )
            if self.__bedtime.hour == self.__asleep.hour and self.__bedtime.minute > self.__asleep.minute:
                raise ValueError("Не можешь в рамках часа уснуть раньше чем лег на кровать!")
            elif datetime_asleep - datetime_bedtime > timedelta(hours=12):
                raise ValueError("Время отхода ко сну не может быть позже времени засыпания!\n"
                                 "Или время между этими событиями не может быть более 12 часов!")

        without_sleep = self.__without_sleep.hour * 60 + self.__without_sleep.minute
        sleep_duration = get_timedelta(self.__calendar_date, self.__awake, self.__asleep).seconds / 60
        time_in_bed = get_timedelta(self.__calendar_date, self.__rise, self.__bedtime).seconds / 60
        if sleep_duration < without_sleep:
            raise ValueError('Время проведенное без сна не может быть больше времени сна')
        if time_in_bed < sleep_duration:
            raise ValueError('Время проведенное в кровати не может быть меньше времени сна.')

    @staticmethod
    def create_entry():
        new_entry = DiaryEntryManager(
            request.form['calendar_date'],
            request.form['bedtime'],
            request.form['asleep'],
            request.form['awake'],
            request.form['rise'],
            request.form['without_sleep']
        )
        notation = Notation(
            calendar_date=new_entry.__calendar_date,
            bedtime=new_entry.__bedtime,
            asleep=new_entry.__asleep,
            awake=new_entry.__awake,
            rise=new_entry.__rise,
            without_sleep=new_entry.__without_sleep,
            user_id=current_user.id
        )
        return notation

    @staticmethod
    def get_all_diary_entries():
        notations = get_all_notations_of_user()
        list_of_instances = []
        for notation in notations:
            get_diary_entry = DiaryEntryManager(
                notation.calendar_date,
                notation.bedtime,
                notation.asleep,
                notation.awake,
                notation.rise,
                notation.without_sleep
            )
            list_of_instances.append(get_diary_entry)
        return list_of_instances

    @property
    def calendar_date(self):
        if isinstance(self.__calendar_date, date):
            return f'{self.__calendar_date:%Y-%m-%d}'
        else:
            return None

    @calendar_date.setter
    def calendar_date(self, set_date):
        if set_date is None:
            self.__calendar_date = None
        elif isinstance(set_date, str):
            self.__calendar_date = datetime.strptime(set_date, "%Y-%m-%d")
        elif isinstance(set_date, date):
            self.__calendar_date = set_date
        else:
            raise TypeError('Ошибка типа данных даты.')

    @property
    def bedtime(self):
        if isinstance(self.__bedtime, time):
            return f"{self.__bedtime:{TIME_FORMAT}}"
        else:
            return None

    @bedtime.setter
    def bedtime(self, set_time: Optional[time]):
        if set_time is None:
            self.__bedtime = None
        elif isinstance(set_time, time):
            self.__bedtime = set_time
        elif isinstance(set_time, str):
            self.__bedtime = str_to_time(set_time)
        else:
            raise TypeError('Ошибка типа данных даты.')

    @property
    def asleep(self):
        if isinstance(self.__asleep, time):
            return f"{self.__asleep:{TIME_FORMAT}}"
        else:
            return None

    @asleep.setter
    def asleep(self, set_time: Optional[time]):
        if set_time is None:
            self.__asleep = None
        elif isinstance(set_time, time):
            self.__asleep = set_time
        elif isinstance(set_time, str):
            self.__asleep = str_to_time(set_time)
        else:
            raise TypeError('Ошибка типа данных времени.')

    @property
    def awake(self):
        if isinstance(self.__awake, time):
            return f"{self.__awake:{TIME_FORMAT}}"
        else:
            return None

    @awake.setter
    def awake(self, set_time: Optional[time]):
        if set_time is None:
            self.__awake = None
        elif isinstance(set_time, time):
            self.__awake = set_time
        elif isinstance(set_time, str):
            self.__awake = str_to_time(set_time)
        else:
            raise TypeError('Ошибка типа данных времени.')

    @property
    def rise(self):
        if isinstance(self.__rise, time):
            return f"{self.__rise:{TIME_FORMAT}}"
        else:
            return None

    @rise.setter
    def rise(self, set_time: Optional[time]):
        if set_time is None:
            self.__rise = None
        elif isinstance(set_time, time):
            self.__rise = set_time
        elif isinstance(set_time, str):
            self.__rise = str_to_time(set_time)
        else:
            raise TypeError('Ошибка типа данных времени.')

    @property
    def without_sleep(self):
        if isinstance(self.__without_sleep, time):
            return f"{self.__without_sleep:{TIME_FORMAT}}"
        else:
            return None

    @without_sleep.setter
    def without_sleep(self, set_time):
        if set_time is None:
            self.__without_sleep = None
        elif isinstance(set_time, str):
            self.__without_sleep = str_to_time(set_time)
        elif isinstance(set_time, time):
            self.__without_sleep = set_time
        else:
            raise TypeError('Ошибка типа данных времени.')

    @property
    def sleep_duration(self):
        if self.__calendar_date is None:
            return None
        else:
            return self.get_sleep_duration()
