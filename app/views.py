import csv
from app import app
from datetime import datetime, time, date
from flask import render_template, request, redirect, send_file
from .models import *
from .config import Errors

# todo Узнать насчет except, разобраться и доделать
# todo Разбить это файл на 2: routes, functions(попробовать забрать отсюда все функции)


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


@app.route('/sleep')
def sleep_dairy():
    """Отображает все записи дневника сна из базы данных"""

    # todo Поправить логику связанную с тем, что используется id. Если 1 день не создать notation,
    #  то все соотношения сдвинутся
    def average_sleep_efficiency_per_week(week_number):
        """Вычисляет среднюю эффективность сна за неделю"""
        sum_of_efficiency, week_length = 0, 0
        first_day_of_week = 7 * (week_number - 1) + 1
        last_day_of_week = 8 * week_number - (week_number - 1)
        for day in range(first_day_of_week, last_day_of_week):
            # todo мб вместо elem использовать временную notation
            for elem in notations:
                # todo почему elem.id, а не elem.data???
                if elem.id != day:
                    continue
                week_length += 1
                if elem.sleep_duration != 0:
                    sum_of_efficiency += elem.sleep_duration / elem.time_in_bed
        if week_length == 0:
            return 0
        return round(((sum_of_efficiency / week_length) * 100), 2)

    def average_sleep_duration_per_week(week_number):
        """Вычисляет среднюю продолжительность сна за неделю"""
        sum_of_minutes, week_length = 0, 0
        first_day_of_week = 7 * (week_number - 1) + 1
        last_day_of_week = 8 * week_number - (week_number - 1)
        for day in range(first_day_of_week, last_day_of_week):
            for elem in notations:
                # print(type(elem.id))
                if elem.id != day:
                    continue
                week_length += 1
                sum_of_minutes += elem.sleep_duration
        if week_length == 0:
            return 0
        return int(sum_of_minutes / week_length)

    def check_notations(week_number):
        amount = 0
        first_day_of_week = 7 * (week_number - 1) + 1
        last_day_of_week = 8 * week_number - (week_number - 1)
        for day in range(first_day_of_week, last_day_of_week):
            for elem in notations:
                if elem.id != day:
                    continue
                amount += 1
        if amount == 0:
            return 0
        return amount

    def last_day(day_number: int):
        if day_number == db_elem_counter:
            return True
        return False

    def today_date():
        """Возвращает текущую локальную дату в формате 'YYYY-MM-DD'"""
        return datetime.date(datetime.today())

    # todo добавить аннотацию. мб название сделать all_notations?
    # todo сортировка по id не имеет смысла, так как записи добавляются по автоинкрементному id и
    #  уже отсортированы по возрастанию id
    notations = db.session.query(Notation).order_by(Notation.id)
    db_elem_counter = db.session.query(Notation).count()

    return render_template("sleep.html", notations=notations, time_display=time_display,
                           average_sleep_duration_per_week=average_sleep_duration_per_week,
                           sleep_efficiency=sleep_efficiency, db_elem_counter=db_elem_counter,
                           average_sleep_efficiency_per_week=average_sleep_efficiency_per_week,
                           check_notations=check_notations, last_day=last_day, today_date=today_date)


@app.route('/sleep', methods=['POST', 'GET'])
def add_notation():
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
            db.session.commit()
            return redirect('/')
        except (Exception, ):
            return "При добавлении статьи произошла ошибка"
    elif request.method == "GET":
        return render_template('sleep.html')


@app.route('/sleep/<int:delete_id>/delete')
def delete_notation(delete_id):
    notation = Notation.query.get_or_404(delete_id)
    try:
        db.session.delete(notation)
        db.session.commit()
        return redirect('/sleep')
    except (Exception, ):
        return "При удалении записи произошла ошибка"


@app.route('/sleep/<int:update_id>/update', methods=['POST', 'GET'])
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


# todo разбит на несколько функций
@app.route('/edit', methods=['POST', 'GET'])
def edit_dairy():
    # todo сортировка по id не имеет смысла, так как записи добавляются по автоинкрементному id и
    #  уже отсортированы по возрастанию id
    notations = db.session.query(Notation).order_by(Notation.id)
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
                    # todo rename elem to notation
                    for elem in notations:
                        writer.writerow([
                            elem.calendar_date, elem.bedtime.strftime('%H:%M'), elem.asleep.strftime('%H:%M'),
                            elem.awake.strftime('%H:%M'), elem.rise.strftime('%H:%M'), elem.without_sleep,
                            elem.sleep_duration,
                            elem.time_in_bed, sleep_efficiency(elem.sleep_duration, elem.time_in_bed)
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
                        except (Exception, ):
                            return f"add"
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
