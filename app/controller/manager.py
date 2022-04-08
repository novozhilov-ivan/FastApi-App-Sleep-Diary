from datetime import datetime, time, date, timedelta

from flask import render_template, request, redirect, url_for, flash

from app.controller import *


# notation = Notation.add_notation_and_commit(
#     request.form.form['calendar_date'],
#     request.form['bedtime'],
#     request.form['asleep'],
#     request.form['awake'],
#     request.form['rise'],
#     request.form['without_sleep']
# )

class DiaryEntryManager:
    def __init__(self, calendar_date=None, bedtime=None, asleep=None, awake=None, rise=None,
                 without_sleep=None, sleep_duration=None, time_in_bed=None):
        self.calendar_date = calendar_date
        self.bedtime = bedtime
        self.asleep = asleep
        self.awake = awake
        self.rise = rise
        self.without_sleep = without_sleep
        self.sleep_duration = sleep_duration
        self.time_in_bed = time_in_bed

        if self.calendar_date is not None:
            sleep_time_check(self.calendar_date, self.bedtime, self.asleep)
            wake_up_time_check(self.calendar_date, self.awake, self.rise)
            sleep_duration_less_time_in_bed(
                self.calendar_date, self.bedtime, self.asleep, self.awake, self.rise
            )
        print(f"\n\nЗаготовка для записи: "
              f"[Дата: {self.calendar_date}, Лег: {self.bedtime},"
              f" Уснул: {self.asleep}, Проснулся: {self.awake},"
              f" Встал: {self.rise}, Не спал: {self.without_sleep}]\n\n")

    def __repr__(self):
        return f"\n\nЗаготовка для записи: " \
               f"[Дата: {self.calendar_date}, Лег: {self.bedtime}," \
               f" Уснул: {self.asleep}, Проснулся: {self.awake}," \
               f" Встал: {self.rise}, Не спал: {self.without_sleep}]\n\n"

    def get_forms_data_and_reformat(self):
        self.calendar_date = datetime.strptime(request.form['calendar_date'], "%Y-%m-%d")
        self.bedtime = str_to_time(request.form['bedtime'][:5])
        self.asleep = str_to_time(request.form['asleep'][:5])
        self.awake = str_to_time(request.form['awake'][:5])
        self.rise = str_to_time(request.form['rise'][:5])
        self.without_sleep = str_to_time(request.form['without_sleep'][:5])
        return DiaryEntryManager(
            self.calendar_date, self.bedtime, self.asleep, self.awake, self.rise, self.without_sleep
        )

    @staticmethod
    def get_sleep_diary():
        all_notations_of_user = get_all_notations_of_user()
        amount_diary_entry = len(all_notations_of_user)
        list_of_diary_entry = []
        for i in range(amount_diary_entry):
            pass
