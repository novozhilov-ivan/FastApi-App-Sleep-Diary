import csv
import os
from datetime import datetime, time, date

import sqlalchemy.exc
from flask import request, redirect, send_file, url_for, flash

from .routes import current_user
from .config import Errors, db
from .models import Notation
from .exception import SleepLessTimeInBedError


def analyze_week(week_number):
    """
    По номеру недели рассчитывает ее длину в днях, количество записей, суммарную эффективность за все дни недели,
    суммарное время сна за все дни недели.
    """
    sum_of_minutes, sum_of_efficiency, week_length, amount = 0, 0, 0, 0
    first_day_of_week = 7 * (week_number - 1) + 1
    last_day_of_week = 8 * week_number - (week_number - 1)
    all_notations = db.session.query(Notation).order_by(Notation.calendar_date).filter_by(user_id=current_user.id)
    for day in range(first_day_of_week, last_day_of_week):
        for day_number, _notation in enumerate(all_notations, start=1):
            if day_number != day:
                continue
            week_length += 1
            amount += 1
            sum_of_minutes += _notation.sleep_duration
            if _notation.sleep_duration != 0:
                sum_of_efficiency += _notation.sleep_duration / _notation.time_in_bed
    return week_length, amount, sum_of_efficiency, sum_of_minutes


def get_average_sleep_efficiency_per_week(week_number):
    """Вычисляет среднюю эффективность сна за неделю"""
    week_length, sum_of_efficiency = analyze_week(week_number)[0], analyze_week(week_number)[2]
    if week_length == 0:
        return 0
    return round(((sum_of_efficiency / week_length) * 100), 2)


def get_average_sleep_duration_per_week(week_number):
    """Вычисляет среднюю продолжительность сна за неделю"""
    week_length, sum_of_minutes = analyze_week(week_number)[0], analyze_week(week_number)[3]
    if week_length == 0:
        return 0
    return int(sum_of_minutes / week_length)


def get_amount_notations_of_week(week_number):
    """Рассчитывает количество добавленных записей в неделе"""
    amount = analyze_week(week_number)[1]
    if amount == 0:
        return 0
    return amount


def today_date():
    """Возвращает текущую локальную дату в формате 'YYYY-MM-DD'"""
    return datetime.date(datetime.today())


def str_to_time(string_time: str):
    """Изменяет тип данных str на time в формате 'HH:MM'"""
    return datetime.time(datetime.strptime(string_time, '%H:%M'))


def str_to_date(string_date: str):
    """Изменяет тип данных str на date в формате 'YYYY-MM-DD'"""
    return datetime.date(datetime.strptime(string_date, '%Y-%m-%d'))


def sleep_efficiency(sleep_duration: int, time_in_bed: int):
    """Вычисляет эффективность сна(отношение времени сна к времени нахождения в кровати) в процентах"""
    if sleep_duration == 0:
        return 0
    return round((sleep_duration / time_in_bed) * 100, 2)


def time_display(time_point: int or time):
    """Конвертирует время из типа данных int или time в str в формате 'HH:MM'"""
    if isinstance(time_point, int):
        if time_point % 60 < 10:
            return str(time_point // 60) + ':0' + str(time_point % 60)
        return str(time_point // 60) + ':' + str(time_point % 60)
    elif isinstance(time_point, time):
        return time_point.strftime('%H:%M')
    else:
        raise TypeError


def get_timedelta(calendar_date: date, time_point_1: time, time_point_2: time):
    """Получает временной интервал между двумя точками, каждая из которых скомбинирована из даты с времени"""
    return datetime.combine(calendar_date, time_point_1) - datetime.combine(calendar_date, time_point_2)


def edit_diary_export():
    """Сохраняет все записи дневника из базы данных в csv-файл"""
    all_notations = db.session.query(Notation).order_by(Notation.calendar_date)
    try:
        with open("app/export_diary.csv", "w", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow((
                'Дата', 'Лег', 'Уснул', 'Проснулся', 'Встал',
                'Не спал', 'Время сна', 'Время в кровати',
                'Эффективность сна'
            ))
            for notation in all_notations:
                writer.writerow([
                    notation.calendar_date, notation.bedtime.strftime('%H:%M'),
                    notation.asleep.strftime('%H:%M'), notation.awake.strftime('%H:%M'),
                    notation.rise.strftime('%H:%M'), notation.without_sleep,
                    notation.sleep_duration, notation.time_in_bed,
                    sleep_efficiency(notation.sleep_duration, notation.time_in_bed)
                ])
        return send_file("export_diary.csv")
    except (Exception,):
        flash("При экспортировании произошла ошибка")
        return redirect(url_for('edit_diary'))
    finally:
        os.remove("app/export_diary.csv")


def edit_diary_import():
    """Импортирует записи из csv-файла в базу данных"""
    try:
        count = 0
        with open('import_file.csv', "r", encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                calendar_date = datetime.date(datetime.strptime(row[0], '%Y-%m-%d'))
                bedtime = str_to_time(row[1])
                asleep = str_to_time(row[2])
                awake = str_to_time(row[3])
                rise = str_to_time(row[4])
                without_sleep = int(row[5])
                sleep_duration = get_timedelta(calendar_date, awake, asleep).seconds / 60 - without_sleep
                time_in_bed = get_timedelta(calendar_date, rise, bedtime).seconds / 60
                notation = Notation(calendar_date=calendar_date, sleep_duration=sleep_duration, rise=rise,
                                    time_in_bed=time_in_bed, bedtime=bedtime, asleep=asleep, awake=awake,
                                    without_sleep=without_sleep, user_id=current_user.id)
                try:
                    db.session.add(notation)
                    db.session.commit()
                    count += 1
                except sqlalchemy.exc.IntegrityError:
                    flash('Ошибка при добавлении записей в базу данных. Даты записей должны быть уникальными.')
                except (Exception,):
                    flash('Ошибка при добавлении записей в базу данных. Прочая ошибка')
        flash(f"Успешно импортировано записей: {count}")
        return redirect(url_for('sleep_diary'))
    except TypeError:
        flash(f"{Errors['import']}: {Errors['type']}")
    except ValueError:
        flash(f"{Errors['import']}: {Errors['value']}")
    except SyntaxError:
        flash(f"{Errors['import']}: {Errors['syntax']}")
    except FileNotFoundError:
        flash(f"{Errors['import']}: {Errors['file']}")
    except (Exception,):
        flash(f"{Errors['import']}: {Errors['other']}")
    finally:
        return redirect(url_for('edit_diary')), os.remove('import_file.csv')


def edit_diary_delete_all_notations():
    """Удаляет все записи из базы данных"""
    try:
        db.session.query(Notation).delete()
        db.session.commit()
        flash("Все записи успешно удалены")
        return redirect(url_for('edit_diary'))
    except (NameError, TypeError):
        flash("При удалении записей из базы данных произошла ошибка SQLAlchemy")
        return redirect(url_for('edit_diary'))
    except (Exception,):
        flash("При удалении записей из базы данных произошла ошибка: Прочая ошибка")
        return redirect(url_for('edit_diary'))


def edit_notation_update(notation_date: str):
    """Обновление одной записи в дневнике сна/базе данных"""

    notation = db.session.query(Notation).filter_by(user_id=current_user.id, calendar_date=notation_date).first()
    notation.bedtime = str_to_time(request.form['bedtime'][:5])
    notation.asleep = str_to_time(request.form['asleep'][:5])
    notation.awake = str_to_time(request.form['awake'][:5])
    notation.rise = str_to_time(request.form['rise'][:5])
    without_sleep = str_to_time(request.form['without_sleep'])
    notation.without_sleep = without_sleep.hour * 60 + without_sleep.minute
    sleep_duration = get_timedelta(notation.calendar_date, notation.awake, notation.asleep)
    time_in_bed = get_timedelta(notation.calendar_date, notation.rise, notation.bedtime)
    notation.sleep_duration = sleep_duration.seconds / 60 - notation.without_sleep
    notation.time_in_bed = time_in_bed.seconds / 60

    try:
        if notation.time_in_bed < notation.sleep_duration:
            raise SleepLessTimeInBedError

        db.session.commit()
        flash(f'Запись {notation.calendar_date} успешно обновлена')
        return redirect(url_for('sleep_diary'))
    except SleepLessTimeInBedError:
        flash('Ошибка данных. Время проведенное в кровати не может быть меньше времени сна.')
    except (Exception,):
        flash('При обновлении записи произошла ошибка')
    finally:
        return redirect(f'/sleep/update/{notation.calendar_date}')


def delete_notation(delete_notation_date: str):
    """Удаление одной записи дневника из дневника сна/базы данных"""
    notation = Notation.query.get(str_to_date(delete_notation_date))
    try:
        db.session.delete(notation)
        db.session.commit()
        flash(f'Запись {delete_notation_date} успешно удалена')
        return redirect(url_for('sleep_diary'))
    except (Exception,):
        flash(f'При удалении записи {delete_notation_date} произошла ошибка')
        return redirect(url_for(f'/sleep/update/<{delete_notation_date}>'))
