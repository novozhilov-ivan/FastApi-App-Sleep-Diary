import csv
from datetime import datetime, time, date

import sqlalchemy.exc
from flask import render_template, request, redirect, send_file

from .config import Errors
from .models import *


# todo Узнать насчет except, разобраться и доделать
# todo Разбить это файл на 2: routes, functions(попробовать забрать отсюда все функции)
# todo Разобраться с ошибкой update и delete (мб связано с с тем что брать записи нужно по первичному ключу)
# todo кроме первой недели аккордион не работает


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
        if notation.id is None and check == 0:
            check += 1
            notation.id = check
        else:
            check += 1
            notation.id = check
    try:
        db.session.commit()
        return 'Переиндексированные записи успешно сохранены в базу данных'
    except (Exception, ):
        return 'Ошибка сохранения переиндексированных записей в базу данных'


@app.route('/sleep', methods=['POST', 'GET'])
def sleep_dairy():
    """Отображает все записи дневника сна из базы данных"""
    # id_notations_update()
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
            # db.session.commit()
            id_notations_update()
            return redirect('/')
        except sqlalchemy.exc.IntegrityError:
            return "При добавлении записи в базу данных произошла ошибка. Дата записи должна быть уникальной."
        except (Exception, ):
            return "При добавлении записи в базу данных произошла ошибка. Прочая ошибка"
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
                               check_notations=check_notations, last_day=db_notation_counter, today_date=today_date)


@app.route('/sleep/<int:delete_id>/delete')
def delete_notation(delete_id):
    notation = Notation.query.get(delete_id)
    try:
        db.session.delete(notation)
        db.session.commit()
        return redirect('/sleep')
    except (Exception, ):
        return "При удалении записи произошла ошибка"


@app.route('/sleep/<int:update_id>/update', methods=['POST', 'GET', 'PUT'])
def update(update_id):
    notation = Notation.query.get(update_id)
    if request.method == "POST":
        notation.calendar_date = str_to_date(request.form['calendar_date'])
        notation.bedtime = str_to_time(request.form['bedtime'])
        notation.asleep = str_to_time(request.form['asleep'])
        notation.awake = str_to_time(request.form['awake'])
        notation.rise = str_to_time(request.form['rise'])
        without_sleep = str_to_time(request.form['without_sleep'])
        notation.without_sleep = without_sleep.hour * 60 + without_sleep.minute
        sleep_duration = get_timedelta(notation.calendar_date, notation.awake, notation.asleep)
        time_in_bed = get_timedelta(notation.calendar_date, notation.rise, notation.bedtime)
        notation.sleep_duration = sleep_duration.seconds / 60 - notation.without_sleep
        notation.time_in_bed = time_in_bed.seconds / 60
        try:
            db.session.commit()
            return redirect('/sleep')
        except Exception as err:
            return err
    elif request.method == "GET":
        return render_template("notation_update.html", notation=notation)


# todo разбить на несколько функций

@app.route('/edit', methods=['POST', 'GET'])
def edit_dairy():
    all_notations = db.session.query(Notation).order_by(Notation.id)
    if request.method == 'POST':
        if request.form.get('export') == 'Экспортировать дневник':
            try:
                with open("../export_dairy.csv", "w", encoding='utf-8') as file:
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
                return send_file('../export_dairy.csv')
            except (Exception, ):
                return "При экспортировании произошла ошибка"
        elif request.form.get('import') == 'Импортировать дневник':
            try:
                count = 0
                with open(request.form['importfile'], "r") as file:
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
                            db.session.commit()
                            count += 1
                        except sqlalchemy.exc.IntegrityError:
                            return "Ошибка при добавлении записей в базу данных. Даты записей должны быть уникальными."
                        except (Exception, ):
                            return "Ошибка при добавлении записей в базу данных. Прочая ошибка"
                    return f"Успешно импортировано записей: {count}"
            except TypeError:
                return f"{Errors['import']}: {Errors['type']}"
            except ValueError:
                return f"{Errors['import']}: {Errors['value']}"
            except SyntaxError:
                return f"{Errors['import']}: {Errors['syntax']}"
            except FileNotFoundError:
                return f"{Errors['import']}: {Errors['file']}"
            except (Exception, ):
                return f"{Errors['import']}: {Errors['other']}"
        elif request.form.get('delete_dairy') == 'Удалить дневник':
            try:
                db.session.query(Notation).delete()
                db.session.commit()
                return "Все записи успешно удалены"
            except (NameError, TypeError):
                return "При удалении записей из базы данных произошла ошибка SQLAlchemy"
            except Exception as error:
                return error
    elif request.method == "GET":
        return render_template("edit_dairy.html")


@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html")
