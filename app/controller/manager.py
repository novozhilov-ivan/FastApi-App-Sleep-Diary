from datetime import datetime, time, date, timedelta

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.controller import *
from app.model import *


class DiaryEntryManager:
    def __init__(self, calendar_date=None, bedtime=None, asleep=None, awake=None, rise=None,
                 without_sleep=None, sleep_duration=None, time_in_bed=None):
        self.calendar_date = calendar_date
        self._bedtime = bedtime
        self._asleep = asleep
        self._awake = awake
        self._rise = rise
        self._without_sleep = without_sleep
        self._sleep_duration = sleep_duration
        self._time_in_bed = time_in_bed

        if self.calendar_date is not None:
            sleep_time_check(self.calendar_date, self._bedtime, self._asleep)
            wake_up_time_check(self.calendar_date, self._awake, self._rise)
            sleep_duration_less_time_in_bed(self.calendar_date, self._bedtime, self._asleep, self._awake, self._rise)

    def __repr__(self):
        return f"\n\nЗаготовка для записи: [Дата: {self.calendar_date}, Лег: {self._bedtime}, Уснул: {self._asleep}," \
               f" Проснулся: {self._awake}, Встал: {self._rise}, Не спал: {self._without_sleep}]\n\n"

    # это получился сеттер но тут будет геттер
    @property
    def diary_entry(self):
        self.calendar_date = datetime.strptime(request.form['calendar_date'], "%Y-%m-%d")
        self._bedtime = str_to_time(request.form['bedtime'][:5])
        self._asleep = str_to_time(request.form['asleep'][:5])
        self._awake = str_to_time(request.form['awake'][:5])
        self._rise = str_to_time(request.form['rise'][:5])
        self._without_sleep = str_to_time(request.form['without_sleep'][:5])
        # плюс рассчитанные значения из верхних
        return Notation(
            calendar_date=self.calendar_date, bedtime=self._bedtime, asleep=self._asleep,
            awake=self._awake, rise=self._rise, without_sleep=self._without_sleep,
            user_id=current_user.id
        )
    # в целом не то что нужно
    @diary_entry.setter
    def diary_entry(self):
        self.calendar_date = datetime.strptime(request.form['calendar_date'], "%Y-%m-%d")
        self._bedtime = str_to_time(request.form['bedtime'][:5])
        self._asleep = str_to_time(request.form['asleep'][:5])
        self._awake = str_to_time(request.form['awake'][:5])
        self._rise = str_to_time(request.form['rise'][:5])
        self._without_sleep = str_to_time(request.form['without_sleep'][:5])
        # плюс рассчитанные значения из верхних
        Notation(
            calendar_date=self.calendar_date, bedtime=self._bedtime, asleep=self._asleep,
            awake=self._awake, rise=self._rise, without_sleep=self._without_sleep,
            user_id=current_user.id
        )

    @staticmethod
    def get_sleep_diary():
        all_notations_of_user = get_all_notations_of_user()
        amount_diary_entry = len(all_notations_of_user)
        list_of_diary_entry = []
        for i in range(amount_diary_entry):
            pass
