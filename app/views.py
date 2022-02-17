import csv
from datetime import datetime, time, date

import sqlalchemy.exc
from flask import render_template, request, redirect, send_file, url_for, flash

from app import app, Errors
from .models import *


# TODO добавить в функции экспорта и импорта удаление созданных csv-файлов в каталоге
# todo кроме первой недели аккордеон не работает
# todo вставить везде флеши


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
    return round((sleep_duration / time_in_bed * 100), 2)


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


def id_notations_update():
    """Перезаписывает все id в бд согласно очередности дат записей"""
    all_notations = db.session.query(Notation).order_by(Notation.calendar_date).all()
    check = 0
    for notation in all_notations:
        check += 1
        notation.id = check
    try:
        db.session.commit()
        return 'Переиндексированные записи успешно сохранены в базу данных'
    except (Exception, ):
        return 'Ошибка сохранения переиндексированных записей в базу данных'


def edit_diary_export():
    """Сохраняет все записи дневника из базы данных в csv-файл"""
    all_notations = db.session.query(Notation).order_by(Notation.id)
    try:
        with open("export_diary.csv", "w", encoding='utf-8') as file:
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
        return send_file('export_diary.csv')
    except (Exception,):
        flash("При экспортировании произошла ошибка")
        return redirect(url_for('edit_diary'))


def edit_diary_import():
    """Импортирует записи из csv-файла в базу данных"""
    try:
        count = 0
        with open('importfile.csv', "r", encoding='utf-8') as file:
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
                                    without_sleep=without_sleep)
                try:
                    db.session.add(notation)
                    id_notations_update()
                    count += 1
                except sqlalchemy.exc.IntegrityError:
                    flash('Ошибка при добавлении записей в базу данных. Даты записей должны быть уникальными.')
                except (Exception, ):
                    flash('Ошибка при добавлении записей в базу данных. Прочая ошибка')
            flash(f"Успешно импортировано записей: {count}")
    except TypeError:
        flash(f"{Errors['import']}: {Errors['type']}")
    except ValueError:
        flash(f"{Errors['import']}: {Errors['value']}")
    except SyntaxError:
        flash(f"{Errors['import']}: {Errors['syntax']}")
    except FileNotFoundError:
        flash(f"{Errors['import']}: {Errors['file']}")
    except (Exception, ):
        flash(f"{Errors['import']}: {Errors['other']}")
    finally:
        return redirect(url_for('edit_diary'))


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
    except (Exception, ):
        flash("При удалении записей из базы данных произошла ошибка: Прочая ошибка")
        return redirect(url_for('edit_diary'))


def edit_notation_update(notation_date: str):
    """Обновление одной записи в дневнике сна/базе данных"""
    notation = Notation.query.get(str_to_date(notation_date))
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
        db.session.commit()
        id_notations_update()
        flash(f'Запись {notation.calendar_date} успешно обновлена')
        return redirect(url_for('sleep_diary'))
    except (Exception,):
        flash('При обновлении записи произошла ошибка')
        return edit_notation(notation.calendar_date)


def delete_notation(delete_notation_date: str):
    """Удаление одной записи дневника из дневника сна/базы данных"""
    notation = Notation.query.get(str_to_date(delete_notation_date))
    try:
        db.session.delete(notation)
        id_notations_update()
        flash(f'Запись {delete_notation_date} успешно удалена')
        return redirect(url_for('sleep_diary'))
    except (Exception, ):
        flash(f'При удалении записи {delete_notation_date} произошла ошибка')
        return redirect(url_for(f'/sleep/update/<{delete_notation_date}>'))


@app.route('/sleep', methods=['POST', 'GET'])
def sleep_diary():
    """Отображает все записи дневника сна из базы данных"""
    if request.method == "POST":
        calendar_date = str_to_date(request.form['calendar_date'])
        bedtime = str_to_time(request.form['bedtime'])
        asleep = str_to_time(request.form['asleep'])
        awake = str_to_time(request.form['awake'])
        rise = str_to_time(request.form['rise'])
        without_sleep = str_to_time(request.form['without_sleep'])
        without_sleep = without_sleep.hour * 60 + without_sleep.minute
        sleep_duration = get_timedelta(calendar_date, awake, asleep).seconds / 60 - without_sleep
        time_in_bed = get_timedelta(calendar_date, rise, bedtime).seconds / 60

        notation = Notation(calendar_date=calendar_date, sleep_duration=sleep_duration, time_in_bed=time_in_bed,
                            bedtime=bedtime, asleep=asleep, awake=awake, rise=rise, without_sleep=without_sleep)
        try:
            db.session.add(notation)
            id_notations_update()
            flash('Новая запись успешно добавлена в дневник сна')
            return redirect(url_for('sleep_diary'))
        except sqlalchemy.exc.IntegrityError:
            flash("При добавлении записи в базу данных произошла ошибка. Дата записи должна быть уникальной.")
            return redirect(url_for('sleep_diary'))
        except (Exception, ):
            flash('При добавлении записи в базу данных произошла ошибка. Прочая ошибка')
            return redirect(url_for('sleep_diary'))
    elif request.method == "GET":
        all_notations = db.session.query(Notation).order_by(Notation.calendar_date).all()
        db_notation_counter = db.session.query(Notation).count()

        def average_sleep_efficiency_per_week(week_number):
            """Вычисляет среднюю эффективность сна за неделю"""
            sum_of_efficiency, week_length = 0, 0
            first_day_of_week = 7 * (week_number - 1) + 1
            last_day_of_week = 8 * week_number - (week_number - 1)
            for day in range(first_day_of_week, last_day_of_week):
                for _notation in all_notations:
                    if _notation.id != day:
                        continue
                    week_length += 1
                    if _notation.sleep_duration != 0:
                        sum_of_efficiency += _notation.sleep_duration / _notation.time_in_bed
            if week_length == 0:
                return 0
            return round(((sum_of_efficiency / week_length) * 100), 2)

        def average_sleep_duration_per_week(week_number):
            """Вычисляет среднюю продолжительность сна за неделю"""
            sum_of_minutes, week_length = 0, 0
            first_day_of_week = 7 * (week_number - 1) + 1
            last_day_of_week = 8 * week_number - (week_number - 1)
            for day in range(first_day_of_week, last_day_of_week):
                for _notation in all_notations:
                    if _notation.id != day:
                        continue
                    week_length += 1
                    sum_of_minutes += _notation.sleep_duration
            if week_length == 0:
                return 0
            return int(sum_of_minutes / week_length)

        def check_notations(week_number):
            """Проверка количества записей в неделе"""
            amount = 0
            first_day_of_week = 7 * (week_number - 1) + 1
            last_day_of_week = 8 * week_number - (week_number - 1)
            for day in range(first_day_of_week, last_day_of_week):
                for _notation in all_notations:
                    if _notation.id != day:
                        continue
                    amount += 1
            if amount == 0:
                return 0
            return amount

        def today_date():
            """Возвращает текущую локальную дату в формате 'YYYY-MM-DD'"""
            return datetime.date(datetime.today())

        return render_template("sleep.html", all_notations=all_notations, time_display=time_display,
                               average_sleep_duration_per_week=average_sleep_duration_per_week,
                               sleep_efficiency=sleep_efficiency, db_notation_counter=db_notation_counter,
                               average_sleep_efficiency_per_week=average_sleep_efficiency_per_week,
                               check_notations=check_notations, today_date=today_date)


@app.route('/sleep/update/<notation_date>', methods=['POST', 'GET'])
def edit_notation(notation_date):
    """Редактирование одной записи в дневнике. Удаление всей записи/изменения времени в формах"""
    try:
        notation = Notation.query.get(str_to_date(notation_date))
    except ValueError:
        flash(f'Записи с датой {notation_date} не существует')
        return redirect(url_for('sleep_diary'))
    except (Exception,):
        flash('При загрузки страницы редактирования произошла ошибка')
        return redirect(url_for('sleep_diary'))
    else:
        if request.method == "POST":
            if request.form.get('update_save') == 'Сохранить изменения':
                return edit_notation_update(notation_date)
            elif request.form.get('delete_notation_1') == 'Удалить запись':
                request_delete_notation = True
                flash(f'Вы действительно хотите удалить запись {notation_date} из дневника?')
                return render_template("edit_notation.html", request_delete_notation=request_delete_notation,
                                       notation_date=notation_date, notation=notation)
            elif request.form.get('delete_notation_2') == 'Да, удалить запись из дневника':
                return delete_notation(notation_date)
        elif request.method == "GET":
            return render_template("edit_notation.html", notation=notation)


@app.route('/edit', methods=['POST', 'GET'])
def edit_diary():
    """Вызов функций редактирование дневника сна: экспорт, импорт и удаление всех записей"""
    if request.method == 'POST':
        if request.form.get('export') == 'Экспортировать дневник':
            return edit_diary_export()
        elif request.form.get('import') == 'Импортировать дневник':
            f = request.files['importfile']
            f.save('importfile.csv')
            return edit_diary_import()
        elif request.form.get('delete_diary_1') == 'Удалить дневник':
            request_delete_all_notations = True
            flash('Вы действительно хотите удалить все записи из дневника сна?')
            return render_template("edit_diary.html", request_delete_all_notations=request_delete_all_notations)
        elif request.form.get('delete_diary_2') == 'Да, удалить все записи из дневника':
            return edit_diary_delete_all_notations()
    elif request.method == "GET":
        return render_template("edit_diary.html")


@app.route('/')
@app.route('/main')
def main():
    """Открывает начальную страницу"""
    return render_template("main.html")
