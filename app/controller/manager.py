from datetime import datetime, time, date, timedelta
from typing import Optional, Union

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.controller import *
from app.model import *


# todo по аналогии с временем сна добавить подсчет времени в кровати и эффективности сна за ночь
# todo Добавить метод который возвращает список со средними значениями за неделю


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
            raise TypeError('Неверный тип данных при попытке получить.')

    def __set__(self, instance, value):
        if value is None:
            setattr(instance, self.name, None)
        elif isinstance(value, time):
            setattr(instance, self.name, value)
        elif isinstance(value, str) and len(value) > 8:
            setattr(instance, self.name, str_to_date(value))
        elif isinstance(value, str):
            setattr(instance, self.name, str_to_time(value))
        elif isinstance(value, date):
            setattr(instance, self.name, value)
        else:
            raise TypeError('Неверный тип данных при попытке присвоить.')


class DiaryEntryManager:
    def __repr__(self):
        return f"\n\nЗаготовка для записи: [Дата: {self.calendar_date}, Лег: {self.bedtime}, Уснул: " \
               f"{self.asleep}, Проснулся: {self.awake}, Встал: {self.rise}, Не спал: {self.without_sleep}]\n\n"

    calendar_date = Descriptor()
    bedtime = Descriptor()
    asleep = Descriptor()
    awake = Descriptor()
    rise = Descriptor()
    without_sleep = Descriptor()

    def __init__(self, calendar_date=None, bedtime=None, asleep=None, awake=None, rise=None, without_sleep=None):
        self._calendar_date = calendar_date
        self._bedtime = bedtime
        self._asleep = asleep
        self._awake = awake
        self._rise = rise
        self._without_sleep = without_sleep
        self.__check_timings()
        self.__sleep_duration = None
        self.__in_bed_duration = None
        self.__sleep_efficiency = None

    def _get_sleep_duration(self):
        without_sleep = self._without_sleep.hour * 60 + self._without_sleep.minute
        sleep_timing = get_timedelta(self._calendar_date, self._awake, self._asleep).seconds / 60
        return sleep_timing - without_sleep

    def _get_time_in_bed(self):
        return get_timedelta(self._calendar_date, self._rise, self._bedtime).seconds / 60

    def _get_sleep_efficiency(self):
        sleep_duration = self._get_sleep_duration()
        in_bed_duration = self._get_time_in_bed()
        if sleep_duration == 0:
            return 0
        return round((sleep_duration / in_bed_duration) * 100, 2)

    def __check_timings(self):
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
