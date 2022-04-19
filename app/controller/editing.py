import csv

from flask import redirect, url_for
from flask_login import current_user

from app.controller import *
from app.exception import *
from app.model import *


def export_diary(src):
    """Сохраняет все записи дневника из базы данных в csv-файл"""
    all_notations = get_all_notations_of_user()
    with open(src, "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(('Дата', 'Лег', 'Уснул', 'Проснулся', 'Встал', 'Не спал'))
        for notation in all_notations:
            writer.writerow([
                notation.calendar_date.strftime('%Y-%m-%d'),
                notation.bedtime.strftime('%H:%M'),
                notation.asleep.strftime('%H:%M'),
                notation.awake.strftime('%H:%M'),
                notation.rise.strftime('%H:%M'),
                notation.without_sleep.strftime('%H:%M')
            ])


def find_duplicate_dates_in_file(src: str):
    """Сверяет даты записей из импортируемого файла с датами записей из бд.
    Возвращает список строк с датами записей, которые уже имеются в дневнике
    """
    with open(src, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        dates = [row[0] for row in reader]
    date_of_notations = get_all_dates_of_user()
    exist_dates = [f'{date[0]:%Y-%m-%d}' for date in date_of_notations]
    duplicate_dates = [date for date in dates if date in exist_dates]
    return duplicate_dates


def import_diary(src):
    """
    Импортирует записи из csv-файла в базу данных.
    Возвращает список экземпляров класса, по который были созданы новые записи дневника.
    """
    notations_for_adding = []
    with open(src, "r", encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            notation = Notation(
                calendar_date=str_to_date(row[0]),
                bedtime=str_to_time(row[1]),
                asleep=str_to_time(row[2]),
                awake=str_to_time(row[3]),
                rise=str_to_time(row[4]),
                without_sleep=str_to_time(row[5]),
                user_id=current_user.id
            )
            notations_for_adding.append(notation)
    add_all_and_commit(notations_for_adding)
    return notations_for_adding


def delete_diary():
    """Удаляет все записи пользователя из дневника сна/базы данных"""
    try:
        delete_all_notations()
        flash("Все записи из дневника сна удалены.")
    except (NameError, TypeError):
        flash("При удалении записей из базы данных произошла ошибка SQLAlchemy.")
    except Exception as err:
        display_unknown_error(err)
    finally:
        return redirect(url_for('edit_diary'))
