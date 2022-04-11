import sqlalchemy.exc
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.controller import *
from app.exception import TimeInBedLessSleepError
from app.model import *


@login_required
def create_and_save_entry():
    # try:
    # calendar_date = request.form['calendar_date']
    # bedtime = request.form['bedtime']
    # asleep = request.form['asleep']
    # awake = request.form['awake']
    # rise = request.form['rise']
    # without_sleep = request.form['without_sleep']

    # new_entry = DiaryEntryManager().get_form_data()

    notation = DiaryEntryManager().create_entry()
    add_and_commit(notation)
    flash('Новая запись добавлена в дневник сна')
    # except sqlalchemy.exc.IntegrityError:
    #     flash(f'Запись с датой "{notation.calendar_date}" уже существует.')
    # except TimeInBedLessSleepError:
    #     flash('Время проведенное в кровати не может быть меньше времени сна.')
    # except ValueError as err:
    #     flash(f"{err.args[0]}")
    # except Exception as err:
    #     flash(f'При добавлении записи произошла ошибка. Прочая ошибка. {err.args[0]}')
    # finally:

    # return redirect(url_for('get_main_page'))
    return redirect(url_for('get_sleep_diary_entries'))


# todo поправить отображение(переделать запросы в расчетах средних значений)
@login_required
def render_sleep_diary_page():
    """Отображает все записи дневника сна из БД"""
    all_notations_of_user = get_all_notations_of_user()
    diary_entries = DiaryEntryManager().get_all_diary_entries()

    # print(type(diary_entries[0].calendar_date))
    # print(type(diary_entries[0].__dict__.get('str_calendar_date')))

    # return f'Дата - {diary_entries[0].calendar_date}' \
    #        f' Лег - {diary_entries[0].bedtime}, Уснул - {diary_entries[0].asleep}' \
    #        f' Проснулся - {diary_entries[0].awake}, Встал - {diary_entries[0].rise}' \
    #        f' Не спал - {diary_entries[0].without_sleep}' \
           # f' Длительность сна - {diary_entries[0].sleep_duration}'
    return render_template(
        "sleep.html", time_display=time_display, all_notations=all_notations_of_user,
        average_sleep_duration_per_week=get_average_sleep_duration_per_week,
        sleep_efficiency=sleep_efficiency, amount_notations_of_user=len(all_notations_of_user),
        average_sleep_efficiency_per_week=get_average_sleep_efficiency_per_week,
        get_amount_notations_of_week=get_amount_notations_of_week,
        today_date=today_date, enumerate=enumerate
    )
