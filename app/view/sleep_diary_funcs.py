import sqlalchemy.exc
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import app
from app.controller import *
from app.exception import TimeInBedLessSleepError
from app.model import *


@login_required
def create_and_save_entry():
    calendar_date = str_to_date(request.form['calendar_date'])
    bedtime = str_to_time(request.form['bedtime'])
    asleep = str_to_time(request.form['asleep'])
    awake = str_to_time(request.form['awake'])
    rise = str_to_time(request.form['rise'])
    without_sleep = str_to_time(request.form['without_sleep'])
    without_sleep = without_sleep.hour * 60 + without_sleep.minute
    sleep_duration = get_timedelta(calendar_date, awake, asleep).seconds / 60 - without_sleep
    time_in_bed = get_timedelta(calendar_date, rise, bedtime).seconds / 60
    user_id = current_user.id

    notation = Notation(
        calendar_date=calendar_date, sleep_duration=sleep_duration, time_in_bed=time_in_bed,
        bedtime=bedtime, asleep=asleep, awake=awake, rise=rise, without_sleep=without_sleep,
        user_id=user_id
    )
    try:
        # sleep_time_check()
        if time_in_bed < sleep_duration:
            raise TimeInBedLessSleepError
        add_and_commit(notation)
        flash('Новая запись добавлена в дневник сна')
    except sqlalchemy.exc.IntegrityError:
        flash('При добавлении записи в произошла ошибка.')
        flash(f'Запись с датой "{calendar_date}" уже существует.')
    except TimeInBedLessSleepError:
        flash('Ошибка данных. Время проведенное в кровати не может быть меньше времени сна.')
    except (Exception,):
        flash(f'При добавлении записи произошла ошибка. Прочая ошибка.')
    finally:
        return redirect(url_for('sleep_diary'))


@login_required
def render_sleep_diary_page():
    """Отображает все записи дневника сна из БД"""
    # return controller.Manager.get_sleep_diary()
    all_notations_of_user = get_all_notations_of_user()
    return render_template(
        "sleep.html", time_display=time_display, all_notations=all_notations_of_user,
        average_sleep_duration_per_week=get_average_sleep_duration_per_week,
        sleep_efficiency=sleep_efficiency, amount_notations_of_user=len(all_notations_of_user),
        average_sleep_efficiency_per_week=get_average_sleep_efficiency_per_week,
        get_amount_notations_of_week=get_amount_notations_of_week,
        today_date=today_date, enumerate=enumerate
    )
