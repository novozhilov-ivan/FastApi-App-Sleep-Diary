import csv

from flask_login import current_user

from app.controller import *
from app.model import *


def generate_export_file(src):
    """Сохраняет все записи дневника из базы данных в csv-файл"""
    diary_entries = DiaryEntryManager().diary_entries()
    with open(src, "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            'Дата', 'Лег', 'Уснул', 'Проснулся', 'Встал', 'Не спал',
            'Продолжительность сна', 'Время в кровати', 'Эффективность сна (%)'
        ))
        for entry in diary_entries:
            writer.writerow([
                entry.calendar_date,
                entry.bedtime,
                entry.asleep,
                entry.awake,
                entry.rise,
                entry.without_sleep,
                entry.sleep_duration,
                entry.in_bed_duration,
                entry.sleep_efficiency
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
