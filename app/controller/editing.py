import csv
import os
from datetime import datetime

import sqlalchemy.exc
from flask import request, redirect, send_file, url_for, flash
from flask_login import current_user

from app.config import db
from .get_and_transform_data import sleep_efficiency, str_to_time, get_timedelta
from app.exception import *
from app.model import *


def edit_diary_export():
    """Сохраняет все записи дневника из базы данных в csv-файл"""
    all_notations = db.session.query(Notation).filter_by(user_id=current_user.id).order_by(Notation.calendar_date)
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
    """
    Импортирует записи из csv-файла в базу данных.

    Сверяет даты записей из файла с имеющимися датами записей в базе данных. Если даты с файла не уникальные то,
    не позволяет пользователю импортировать ни одной записи из csv файла, оповещает его об ошибке импортирования и
    указывает не уникальные даты записей, которые необходимо исправить.
    Иначе импортирует записи в базу данных и оповещает о количестве добавленных записей.
    """
    try:
        counter = 0
        string_dates = ''
        list_of_notations_for_commit, list_of_calendar_dates, dates_to_be_corrected = [], [], []
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
                list_of_calendar_dates.append(calendar_date)
                list_of_notations_for_commit.append(notation)
        for new_date in list_of_calendar_dates:
            if db.session.query(Notation).filter_by(user_id=current_user.id, calendar_date=new_date).first() \
                    is not None:
                dates_to_be_corrected.append(new_date.strftime('%Y-%m-%d'))

        try:
            if len(dates_to_be_corrected) != 0:
                string_dates = str(dates_to_be_corrected).replace('[', '').replace(']', '').replace("'", '')
                raise NonUniqueNotationDate
            for notation in list_of_notations_for_commit:
                db.session.add(notation)
                db.session.commit()
                counter += 1
        except sqlalchemy.exc.IntegrityError:
            flash('Ошибка при добавлении записей в базу данных. Даты записей должны быть уникальными.')
        except NonUniqueNotationDate:
            flash('При импортировании произошла ошибка. Повторяющиеся записей.')
            flash(f"Исправьте следующую(ии) запись(и) с датой(ами): "
                  f"{string_dates}. "
                  f"Затем импортируйте файл снова.")
        except (Exception,) as err:
            flash(f'Ошибка при добавлении записей в базу данных. Прочая ошибка. {err}')
        else:
            flash(f"Импортировано записей: {counter}")
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


def edit_diary_delete_all_notations():
    """Удаляет все записи пользователя из дневника сна/базы данных"""
    try:
        db.session.query(Notation).filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash("Все записи из дневника сна удалены.")
        return redirect(url_for('edit_diary'))
    except (NameError, TypeError):
        flash("При удалении записей из базы данных произошла ошибка SQLAlchemy.")
        return redirect(url_for('edit_diary'))
    except (Exception,):
        flash("При удалении записей из базы данных произошла ошибка: Прочая ошибка.")
        return redirect(url_for('edit_diary'))


def edit_notation_update(notation_date: str):
    """Обновление одной записи пользователя в дневнике сна/базе данных"""

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


def delete_notation(delete_notation_date: str):
    """Удаление одной записи пользователя из дневника сна/базы данных"""
    notation = db.session.query(Notation).filter_by(user_id=current_user.id, calendar_date=delete_notation_date).first()
    try:
        db.session.delete(notation)
        db.session.commit()
        flash(f'Запись {delete_notation_date} удалена.')
        return redirect(url_for('sleep_diary'))
    except (Exception,):
        flash(f'При удалении записи {delete_notation_date} произошла ошибка.')
        return redirect(url_for(f'/sleep/update/<{delete_notation_date}>'))
