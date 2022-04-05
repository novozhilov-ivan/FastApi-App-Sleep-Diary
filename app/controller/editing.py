import csv
import os
from datetime import datetime

import sqlalchemy.exc
from flask import request, redirect, send_file, url_for, flash
from flask_login import current_user

from app.config import db
from app.controller import *
from app.exception import *
from app.model import *


def export_diary():
    """Сохраняет все записи дневника из базы данных в csv-файл"""
    all_notations = get_all_notations_of_user()
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


def import_diary():
    """
    Импортирует записи из csv-файла в базу данных.

    Сверяет даты записей из файла с имеющимися датами записей в базе данных. Если даты с файла не уникальные то,
    не позволяет пользователю импортировать ни одной записи из csv файла, оповещает его об ошибке импортирования и
    указывает не уникальные даты записей, которые необходимо исправить.
    Иначе импортирует записи в базу данных и оповещает о количестве добавленных записей.
    """
    try:
        string_dates = ''
        notations_for_adding, all_calendar_dates = [], []
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

                all_calendar_dates.append(calendar_date)
                notations_for_adding.append(notation)
        duplicate_dates = get_duplicate_dates(all_calendar_dates)
        try:
            if duplicate_dates:
                string_dates = str(duplicate_dates).replace('[', '').replace(']', '').replace("'", '')
                raise NonUniqueNotationDate
            add_all_and_commit(notations_for_adding)
        except sqlalchemy.exc.IntegrityError:
            flash('Ошибка при добавлении записей в базу данных. Даты записей должны быть уникальными.')
        except NonUniqueNotationDate:
            flash(f"В импортируемом файле найдены записи с датами, которые уже есть в дневнике. "
                  f"Исправьте записи от: {string_dates}. Затем импортируйте файл снова.")
        except (Exception,) as err:
            flash(f'Ошибка при добавлении записей в базу данных. Прочая ошибка. {err}')
        else:
            flash(f"Импортировано записей: {len(notations_for_adding)}")
            return redirect(url_for('sleep_diary'))
    except TypeError:
        flash(f"{Errors['import']}: {Errors['type']}")
    except ValueError:
        flash(f"{Errors['import']}: {Errors['value']}")
    except SyntaxError:
        flash(f"{Errors['import']}: {Errors['syntax']}")
    except FileNotFoundError:
        flash(f"{Errors['import']}: {Errors['file']}")
    except StopIteration:
        flash('Выберите csv-файл для импорта записей в дневник сна.')
    except (Exception,):
        flash(f"{Errors['import']}: {Errors['other']}")
    finally:
        return redirect(url_for('edit_diary')), os.remove('import_file.csv')


def delete_diary():
    """Удаляет все записи пользователя из дневника сна/базы данных"""
    try:
        delete_all_notations()
        flash("Все записи из дневника сна удалены.")
        return redirect(url_for('edit_diary'))
    except (NameError, TypeError):
        flash("При удалении записей из базы данных произошла ошибка SQLAlchemy.")
        return redirect(url_for('edit_diary'))
    except (Exception,):
        flash("При удалении записей из базы данных произошла ошибка: Прочая ошибка.")
        return redirect(url_for('edit_diary'))


def update_notation(notation: Notation):
    """Обновление одной записи пользователя в дневнике сна/базе данных"""
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
            raise TimeInBedLessSleepError
        db.session.commit()
        flash(f'Запись {notation.calendar_date} обновлена.')
        return redirect(url_for('sleep_diary'))
    except TimeInBedLessSleepError:
        flash('Ошибка данных. Время проведенное в кровати не может быть меньше времени сна.')
    except (Exception,):
        flash('При обновлении записи произошла ошибка.')
    finally:
        return redirect(f'/sleep/update/{notation.calendar_date}')


def delete_notation(notation: Notation):
    """Удаление одной записи пользователя из дневника сна/базы данных"""
    try:
        delete_notation_and_commit(notation)
        flash(f'Запись {notation.calendar_date} удалена.')
        return redirect(url_for('sleep_diary'))
    except (Exception,):
        flash(f'При удалении записи {notation.calendar_date} произошла ошибка.')
        return redirect(url_for(f'/sleep/update/<{notation.calendar_date}>'))
