import math
from datetime import datetime, time, date, timedelta
from typing import Optional

from flask import request
from flask_login import current_user

from app.controller import *
from app.model import *


class Descriptor:
    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        if getattr(instance, self.name) is None:
            return getattr(instance, self.name)
        elif isinstance(getattr(instance, self.name), date):
            return f'{getattr(instance, self.name):%Y-%m-%d}'
        elif isinstance(getattr(instance, self.name), time):
            return f'{getattr(instance, self.name):%H:%M}'
        else:
            raise TypeError('Неверный тип данных при попытке получить значение.')

    def __set__(self, instance, value):
        if value is None:
            setattr(instance, self.name, None)
        elif isinstance(value, time):
            setattr(instance, self.name, value)
        elif isinstance(value, str) and len(value) <= 7:
            setattr(instance, self.name, str_to_time(value))
        elif isinstance(value, str) and len(value) > 8:
            setattr(instance, self.name, str_to_date(value))
        elif isinstance(value, date):
            setattr(instance, self.name, value)
        else:
            raise TypeError('Неверный тип данных при попытке присвоить значение.')


class DiaryEntryManager:
    def __repr__(self):
        return f"\nЗаготовка для записи: [Дата: {self._calendar_date}, Лег: {self._bedtime}, Уснул: " \
               f"{self._asleep}, Проснулся: {self._awake}, Встал: {self._rise}, Не спал: {self._without_sleep}]\n"

    calendar_date = Descriptor()
    bedtime = Descriptor()
    asleep = Descriptor()
    awake = Descriptor()
    rise = Descriptor()
    without_sleep = Descriptor()

    def __init__(
            self, calendar_date=None, bedtime=None, asleep=None, awake=None, rise=None, without_sleep=None,
            average_sleep_duration_per_week=None, average_time_in_bed_per_week=None, week_length=None,
            average_sleep_efficiency_per_week=None
    ):

        self._calendar_date = calendar_date
        self._bedtime = bedtime
        self._asleep = asleep
        self._awake = awake
        self._rise = rise
        self._without_sleep = without_sleep
        self.__check_timings()

        # self.__sleep_duration = None
        # self.__in_bed_duration = None
        # self.__sleep_efficiency = None

        self.__average_sleep_duration_per_week = average_sleep_duration_per_week
        self.__average_time_in_bed_per_week = average_time_in_bed_per_week
        self.__average_sleep_efficiency_per_week = average_sleep_efficiency_per_week
        self.__week_length = week_length

    def _get_sleep_duration(self) -> int:
        without_sleep = self._without_sleep.hour * 60 + self._without_sleep.minute
        sleep_timing = get_timedelta(self._calendar_date, self._awake, self._asleep).seconds / 60
        minutes_amount = int(sleep_timing - without_sleep)
        return minutes_amount

    def _get_time_in_bed(self) -> int:
        return int(get_timedelta(self._calendar_date, self._rise, self._bedtime).seconds / 60)

    def _get_sleep_efficiency(self) -> float:
        sleep_duration = self._get_sleep_duration()
        in_bed_duration = self._get_time_in_bed()
        if sleep_duration == 0:
            return 0
        return round((sleep_duration / in_bed_duration) * 100, 2)

    def __check_timings(self) -> Optional:
        if (self._calendar_date or self._bedtime or self._asleep or self._awake or self._rise) is None:
            return

        if self._bedtime > self._asleep:
            datetime_bedtime = datetime.combine(self._calendar_date, self._bedtime)
            datetime_asleep = datetime.combine(
                date(self._calendar_date.year, self._calendar_date.month, self._calendar_date.day + 1),
                self._asleep
            )
            if self._bedtime.hour == self._asleep.hour and self._bedtime.minute > self._asleep.minute:
                raise ValueError("Не можешь в рамках часа уснуть раньше чем лег на кровать!")
            elif datetime_asleep - datetime_bedtime > timedelta(hours=12):
                raise ValueError("Время отхода ко сну не может быть позже времени засыпания!\n"
                                 "Или время между этими событиями не может быть более 12 часов!")

        if self._awake > self._rise:
            datetime_awake = datetime.combine(self._calendar_date, self._awake)
            datetime_rise = datetime.combine(
                date(self._calendar_date.year, self._calendar_date.month, self._calendar_date.day + 1),
                self._rise
            )
            if self._awake.hour == self._rise.hour and self._awake.minute > self._rise.minute:
                raise ValueError("Не можешь в рамках часа проснуться позже чем встал с кровати!")
            elif datetime_rise - datetime_awake > timedelta(hours=12):
                raise ValueError("Время пробуждения не может быть позже времени подъема с кровати!\n"
                                 "Или время между этими событиями не может быть более 12 часов!")

        without_sleep = self._without_sleep.hour * 60 + self._without_sleep.minute
        sleep_duration = get_timedelta(self._calendar_date, self._awake, self._asleep).seconds / 60
        time_in_bed = get_timedelta(self._calendar_date, self._rise, self._bedtime).seconds / 60
        if sleep_duration < without_sleep:
            raise ValueError('Время проведенное без сна не может быть больше времени сна')
        if time_in_bed < sleep_duration:
            raise ValueError('Время проведенное в кровати не может быть меньше времени сна.')

    def create_entry(self):
        self.calendar_date = request.form['calendar_date']
        self.bedtime = request.form['bedtime']
        self.asleep = request.form['asleep']
        self.awake = request.form['awake']
        self.rise = request.form['rise']
        self.without_sleep = request.form['without_sleep']
        self.__check_timings()

        notation = Notation(
            calendar_date=self._calendar_date,
            bedtime=self._bedtime,
            asleep=self._asleep,
            awake=self._awake,
            rise=self._rise,
            without_sleep=self._without_sleep,
            user_id=current_user.id
        )
        return notation

    @staticmethod
    def diary_entries():
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

    def statistics(self, instances):
        average_values_per_week = []
        amount_of_days = len(instances)
        first_day_of_week = 0
        last_day_of_week = 7

        while amount_of_days > 0:
            sleep_duration_per_week, time_in_bed_per_week, sleep_efficiency_per_week = 0, 0, 0

            if amount_of_days >= 7:
                week_length = 7
                amount_of_days -= 7
            else:
                week_length = amount_of_days
                amount_of_days = 0
                first_day_of_week = first_day_of_week
                last_day_of_week = first_day_of_week + week_length

            for day_number in range(first_day_of_week, last_day_of_week):
                self.calendar_date = instances[day_number].calendar_date
                self.bedtime = instances[day_number].bedtime
                self.asleep = instances[day_number].asleep
                self.awake = instances[day_number].awake
                self.rise = instances[day_number].rise
                self.without_sleep = instances[day_number].without_sleep

                sleep_duration_per_week += self._get_sleep_duration()
                time_in_bed_per_week += self._get_time_in_bed()
                sleep_efficiency_per_week += self._get_sleep_efficiency()

            first_day_of_week += 7
            last_day_of_week += 7

            average_values = DiaryEntryManager(
                average_sleep_duration_per_week=int(sleep_duration_per_week / week_length),
                average_time_in_bed_per_week=int(time_in_bed_per_week / week_length),
                average_sleep_efficiency_per_week=sleep_efficiency_per_week / week_length,
                week_length=week_length
            )
            average_values_per_week.append(average_values)

        return average_values_per_week

    @property
    def sleep_duration(self):
        if self.calendar_date is None:
            return None
        else:
            return time_display(self._get_sleep_duration())

    @property
    def in_bed_duration(self):
        if self.calendar_date is None:
            return None
        else:
            return time_display(self._get_time_in_bed())

    @property
    def sleep_efficiency(self):
        if self.calendar_date is None:
            return None
        else:
            return self._get_sleep_efficiency()

    @property
    def average_sleep_duration_per_week(self):
        return time_display(self.__average_sleep_duration_per_week)

    @property
    def average_time_in_bed_per_week(self):
        return time_display(self.__average_time_in_bed_per_week)

    @property
    def average_sleep_efficiency_per_week(self):
        return f"{self.__average_sleep_efficiency_per_week:.2f}"

    @property
    def week_length(self):
        return self.__week_length
