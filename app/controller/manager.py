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

    def __init__(self, calendar_date=None, bedtime=None, asleep=None, awake=None, rise=None, without_sleep=None,
                 sleep_duration=None):
        self.calendar_date = calendar_date
        self.bedtime = bedtime
        self.asleep = asleep
        self.awake = awake
        self.rise = rise
        self.without_sleep = without_sleep
        if self.__calendar_date is not None:
            self.sleep_duration = sleep_duration
        # self.__correct_wake_up_time(self.__calendar_date, self.__awake, self.__rise)
        # self.__correct_durations(self.__calendar_date, self.__bedtime, self.__asleep, self.__awake, self.__rise)
        # self.__time_in_bed = 0
        # self.__sleep_efficiency = 0.00

    def __repr__(self):
        return f"\n\nЗаготовка для записи: [Дата: {self.__calendar_date}, Лег: {self.__bedtime}, Уснул: " \
               f"{self.__asleep}, Проснулся: {self.__awake}, Встал: {self.__rise}, Не спал: {self.__without_sleep}]\n\n"

    def _sleep_duration(self):
        without_sleep = self.__without_sleep.hour * 60 + self.__without_sleep.minute
        sleep_timing = int(
            (
                    datetime.combine(self.__calendar_date, self.__awake) -
                    datetime.combine(self.__calendar_date, self.__asleep)
            ).seconds / 60
        )
        return time_display(sleep_timing - without_sleep)

    def __correct_sleep_time(self):
        """__correct_sleep_time"""
        if self.__calendar_date or self.__bedtime or self.__asleep is None:
            return None
        # elif isinstance(self.__calendar_date, str):
        #     return self.__calendar_date
        else:
            if self.__bedtime > self.__asleep:
                datetime_bedtime = datetime.combine(self.__calendar_date, self.__bedtime)
                datetime_asleep = datetime.combine(
                    date(self.__calendar_date.year, self.__calendar_date.month, self.__calendar_date.day + 1),
                    self.__asleep
                )
                if self.__bedtime.hour == self.__asleep.hour and self.__bedtime.minute > self.__asleep.minute:
                    raise ValueError("Не можешь в рамках часа уснуть раньше чем лег!")
                elif datetime_asleep - datetime_bedtime > timedelta(hours=12):
                    raise ValueError("Время отхода ко сну не может быть позже времени засыпания!\n"
                                     "Или время между этими событиями не может быть более 12 часов!")
                return datetime_asleep - datetime_bedtime
            return datetime.combine(self.__calendar_date, self.__asleep) - datetime.combine(
                self.__calendar_date,
                self.__bedtime
            )

    @classmethod
    def __correct_wake_up_time(cls, calendar_date, awake, rise):
        """__correct_wake_up_time"""
        if calendar_date or awake or rise is None:
            return None
        if awake > rise:
            datetime_awake = datetime.combine(calendar_date, awake)
            datetime_rise = datetime.combine(date(calendar_date.year, calendar_date.month, calendar_date.day + 1), rise)
            if awake.hour == rise.hour and awake.minute > rise.minute:
                raise ValueError("Не можешь в рамках часа уснуть раньше чем лег!")
            elif datetime_rise - datetime_awake > timedelta(hours=12):
                raise ValueError("Время пробуждения не может быть позже времени подъема с кровати!\n"
                                 "Или время между этими событиями не может быть более 12 часов!")

    @classmethod
    def __correct_durations(cls, calendar_date, bedtime, asleep, awake, rise):
        """__correct_durations"""
        if calendar_date or bedtime or asleep or awake or rise is None:
            return None
        sleep_duration = get_timedelta(calendar_date, awake, asleep).seconds / 60
        time_in_bed = get_timedelta(calendar_date, rise, bedtime).seconds / 60
        if time_in_bed < sleep_duration:
            raise ValueError('Время проведенное в кровати не может быть меньше времени сна.')
        # elif time_in_bed == sleep_duration:
        #     return 0
        # else:
        #     return sleep_efficiency in 0.00

    def get_form_data(self):
        self.calendar_date = request.form['calendar_date']
        self.bedtime = request.form['bedtime']
        self.asleep = request.form['asleep']
        self.awake = request.form['awake']
        self.rise = request.form['rise']
        self.without_sleep = request.form['without_sleep']
        return Notation(
            calendar_date=self.__calendar_date, bedtime=self.__bedtime, asleep=self.__asleep,
            awake=self.__awake, rise=self.__rise, without_sleep=self.__without_sleep, user_id=current_user.id
        )
# todo может изменить, хотя тут только создается класс с правильными форматами атрибутов и возвращается,
# todo а там уже делается коммит


    def get_all_diary_entries(self):
        notations = get_all_notations_of_user()
        list_of_instances = []
        for notation in notations:
            self.calendar_date = notation.calendar_date
            self.bedtime = notation.bedtime
            self.asleep = notation.asleep
            self.awake = notation.awake
            self.rise = notation.rise
            self.without_sleep = notation.without_sleep
            self.sleep_duration = self._sleep_duration()

            list_of_instances.append(
                DiaryEntryManager(
                    self.calendar_date, self.bedtime, self.asleep, self.awake, self.rise,
                    self.without_sleep, self.sleep_duration
                )
            )
        return list_of_instances

    @property
    def calendar_date(self):
        if isinstance(self.__calendar_date, date):
            return f'{self.__calendar_date:%Y-%m-%d}'
        else:
            return None

    @calendar_date.setter
    def calendar_date(self, set_date: Optional[str]):
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
        if isinstance(self.__sleep_duration, time):
            return f"{self.__sleep_duration:{TIME_FORMAT}}"
        else:
            return None

    @sleep_duration.setter
    def sleep_duration(self, set_time):
        self.__sleep_duration = set_time
