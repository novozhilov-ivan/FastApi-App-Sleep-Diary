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
            raise TypeError('Неверный тип данных')

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
            raise TypeError('Ошибка типа данных времени.')


class DiaryEntryManager:
    __TIME_FORMAT = '%H:%M'

    def __repr__(self):
        return f"\n\nЗаготовка для записи: [Дата: {self.calendar_date}, Лег: {self.bedtime}, Уснул: " \
               f"{self.asleep}, Проснулся: {self.awake}, Встал: {self.rise}, Не спал: {self.without_sleep}]\n\n"

    calendar_date = Descriptor()
    bedtime = Descriptor()
    asleep = Descriptor()
    awake = Descriptor()
    rise = Descriptor()
    without_sleep = Descriptor()

# todo подставил один "_" в инициализацию работает, на отдачу, а создание нет. Попробовать поменять убрать статик метод

    def __init__(self, calendar_date=None, bedtime=None, asleep=None, awake=None, rise=None, without_sleep=None):
        self._calendar_date = calendar_date
        self._bedtime = bedtime
        self._asleep = asleep
        self._awake = awake
        self._rise = rise
        self._without_sleep = without_sleep
        self.__sleep_duration = None
        # self.__check_timings()

    def get_sleep_duration(self):
        without_sleep = str_to_time(self.without_sleep)
        calendar_date = str_to_date(self.calendar_date)
        awake = str_to_time(self.awake)
        asleep = str_to_time(self.asleep)

        without_sleep = without_sleep.hour * 60 + without_sleep.minute
        sleep_timing = int(get_timedelta(calendar_date, awake, asleep).seconds / 60)
        return time_display(sleep_timing - without_sleep)

    def __check_timings(self):
        if (self.calendar_date or self.bedtime or self.asleep or self.awake or self.rise) is None:
            return
        calendar_date = str_to_date(self.calendar_date)
        bedtime = str_to_time(self.bedtime)
        asleep = str_to_time(self.asleep)
        awake = str_to_time(self.awake)
        rise = str_to_time(self.rise)
        without_sleep = str_to_time(self.without_sleep)

        if awake > rise:
            datetime_awake = datetime.combine(calendar_date, awake)
            datetime_rise = datetime.combine(
                date(calendar_date.year, calendar_date.month, calendar_date.day + 1),
                rise
            )
            if awake.hour == rise.hour and awake.minute > rise.minute:
                raise ValueError("Не можешь в рамках часа проснуться позже чем встал с кровати!")
            elif datetime_rise - datetime_awake > timedelta(hours=12):
                raise ValueError("Время пробуждения не может быть позже времени подъема с кровати!\n"
                                 "Или время между этими событиями не может быть более 12 часов!")

        if bedtime > asleep:
            datetime_bedtime = datetime.combine(calendar_date, bedtime)
            datetime_asleep = datetime.combine(
                date(calendar_date.year, calendar_date.month, calendar_date.day + 1),
                asleep
            )
            if bedtime.hour == asleep.hour and bedtime.minute > asleep.minute:
                raise ValueError("Не можешь в рамках часа уснуть раньше чем лег на кровать!")
            elif datetime_asleep - datetime_bedtime > timedelta(hours=12):
                raise ValueError("Время отхода ко сну не может быть позже времени засыпания!\n"
                                 "Или время между этими событиями не может быть более 12 часов!")

        without_sleep = without_sleep.hour * 60 + without_sleep.minute
        sleep_duration = get_timedelta(calendar_date, awake, asleep).seconds / 60
        time_in_bed = get_timedelta(calendar_date, rise, bedtime).seconds / 60
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
        # todo тут поменять метод на статик и попробовать создавать через селф._имя
        print(type(new_entry._calendar_date))
        notation = Notation(
            calendar_date=new_entry.calendar_date,
            bedtime=new_entry.bedtime,
            asleep=new_entry.asleep,
            awake=new_entry.awake,
            rise=new_entry.rise,
            without_sleep=new_entry.without_sleep,
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
            return self.get_sleep_duration()
