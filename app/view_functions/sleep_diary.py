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
    # without_sleep = without_sleep.hour * 60 + without_sleep.minute
    # sleep_duration = get_timedelta(calendar_date, awake, asleep).seconds / 60 - without_sleep
    # time_in_bed = get_timedelta(calendar_date, rise, bedtime).seconds / 60
    # new_entry = DiaryEntryManager().get_forms_data_and_reformat()

    # notation = Notation(
    #     calendar_date=new_entry.calendar_date, bedtime=new_entry.bedtime, asleep=new_entry.asleep,
    #     awake=new_entry.awake, rise=new_entry.rise, without_sleep=new_entry.without_sleep,
    #     user_id=current_user.id
    # )
    new_entry = DiaryEntryManager()
    add_and_commit(new_entry.diary_entry)
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
    return redirect(url_for('get_main_page'))
    # return redirect(url_for('get_sleep_diary_entries'))


@login_required
def render_sleep_diary_page():
    """Отображает все записи дневника сна из БД"""
    # sleep_diary = Manager.get_sleep_diary()
    all_notations_of_user = get_all_notations_of_user()

    return render_template(
        "sleep.html", time_display=time_display, all_notations=all_notations_of_user,
        average_sleep_duration_per_week=get_average_sleep_duration_per_week,
        sleep_efficiency=sleep_efficiency, amount_notations_of_user=len(all_notations_of_user),
        average_sleep_efficiency_per_week=get_average_sleep_efficiency_per_week,
        get_amount_notations_of_week=get_amount_notations_of_week,
        today_date=today_date, enumerate=enumerate
    )
