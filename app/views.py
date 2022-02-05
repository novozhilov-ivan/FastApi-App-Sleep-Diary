import csv
from app import app
from datetime import datetime, timedelta, time
from flask import render_template, request, redirect, send_file
from .models import *


# Todo переименовать параметр
def str_to_time(string: str):
    """Изменяет тип данных str на time в формате 'HH:MM'"""
    return datetime.time(datetime.strptime(string, '%H:%M'))


# Todo переименовать параметр
def str_to_ymd(string: str):
    """Изменяет тип данных str на date в формате 'YYYY-MM-DD'"""
    return datetime.date(datetime.strptime(string, '%Y-%m-%d'))


# Todo переименовать функцию
def eff(spal, vkrovati):
    if spal == 0:
        return 0
    return round((spal / vkrovati * 100), 2)


# todo rename
def h_m(vremya: int or datetime):
    if type(vremya) == int:
        if vremya % 60 < 10:
            # todo rename var
            hm = str(vremya // 60) + ':0' + str(vremya % 60)
        else:
            hm = str(vremya // 60) + ':' + str(vremya % 60)
    elif type(vremya) == time:
        hm = vremya.strftime('%H:%M')
    else:
        # raise
        hm = 'TypeError'
    return hm

# # todo rename
# def h_m(vremya: int or datetime):
#     if isinstance(vremya, int):
#         if vremya % 60 < 10:
#             # todo rename var
#             hm = str(vremya // 60) + ':0' + str(vremya % 60)
#         else:
#             hm = str(vremya // 60) + ':' + str(vremya % 60)
#     elif isinstance(vremya, datetime):
#         hm = vremya.strftime('%H:%M')
#     else:
#         raise TypeError
#
#     return hm


def get_timedelta(date1, date2, vremya1, vremya2):
    return datetime.combine(date1, vremya1) - datetime.combine(date2, vremya2)


# todo переименовать.
def date_dmy_to_ymd(s):
    return s[0][6:] + '-' + s[0][3:5] + '-' + s[0][0:2]


@app.route('/sleep')
# todo rename
def basesleep():
    # todo raname "eff"
    # todo добавить докстрингу
    # todo переименовать пераметр
    # todo Поправить логику связанную с тем, что используется id. Если 1 день не созхдать notation,
    #  то все соотношения сдвинутся
    def eff_sleep_of_week(nedelya):
        """Вычисляет среднюю эффективность сна за неделю"""
        sum_eff, elem_of_week = 0, 0

        # todo строка ниже является совсем не очевидной
        for day in range(1 + 7 * (nedelya - 1), 8 * nedelya - (nedelya - 1)):
            # todo мб вместо elem иользовать еременную notation
            for elem in notations:
                # todo почему elem.id, а не elem.data???
                if elem.id != day:
                    continue

                elem_of_week += 1
                if elem.spal != 0:
                    sum_eff += elem.spal / elem.vkrovati

        if elem_of_week == 0:
            return 0
        else:
            return round(((sum_eff / elem_of_week) * 100), 2)

    def avg_duration_sleep_of_week(nedelya):
        sum_min, elem_of_week = 0, 0

        for day in range(1 + 7 * (nedelya - 1), 8 * nedelya - (nedelya - 1)):
            for elem in notations:
                if elem.id == day:
                    elem_of_week += 1
                    sum_min += elem.spal
        if elem_of_week == 0:
            return 0
        else:
            return int(sum_min / elem_of_week)

    def check_notations(nedelya):
        amount = 0
        for day in range(1 + 7 * (nedelya - 1), 8 * nedelya - (nedelya - 1)):
            for elem in notations:
                if elem.id == day:
                    amount += 1
        if amount == 0:
            return 0
        else:
            return amount

    # def last_day(day_number):
    #     day = 0
    #     for elem in notations:
    #         day += 1
    #     if day_number == day:
    #         return True
    #     else:
    #         return False

    def last_day(day_number: int):
        if day_number == db_elem_counter:
            return True
        return False

    # todo функиця наверное не нужна
    def dmy_today():
        return datetime.date(datetime.today())

    # todo добавить аннотацию. мб название сделать all_notations?
    notations = db.session.query(Notation).order_by(Notation.id)
    # todo нет смысла делать 2 запрос. количеством можно получить из первой переменной
    db_elem_counter = db.session.query(Notation).count()

    return render_template("sleep.html", notations=notations, h_m=h_m, eff=eff,
                           db_elem_counter=db_elem_counter,
                           eff_sleep_of_week=eff_sleep_of_week,
                           avg_duration_sleep_of_week=avg_duration_sleep_of_week,
                           check_notations=check_notations, last_day=last_day,
                           dmy_today=dmy_today)


@app.route('/sleep/<int:id>/delete')
def delete_notation(notation_id):
    notations = Notation.query.get_or_404(notation_id)
    try:
        db.session.delete(notations)
        db.session.commit()
        return redirect('/sleep')
    except:
        return "При удалении записи произошла ошибка"


@app.route('/sleep/<int:id>/update', methods=['POST', 'GET'])
def update(update_id):
    # todo неправильное название переменной. ты скорее всего получаегшшь не список а 1 элемент. Переименую переменную
    notations = Notation.query.get(update_id)
    if request.method == "POST":
        notations.date = str_to_ymd(request.form['date'])
        notations.leg = str_to_time(request.form['leg'])
        notations.usnul = str_to_time(request.form['usnul'])
        notations.prosnul = str_to_time(request.form['prosnul'])
        notations.vstal = str_to_time(request.form['vstal'])
        notations.nespal = str_to_time(request.form['nespal']).hour * 60 + str_to_time(request.form['nespal']).minute
        # todo слишком длинное выражение
        delta_spal = datetime.combine(notations.date, notations.prosnul) - datetime.combine(notations.date,
                                                                                            notations.usnul)
        delta_vkrovati = datetime.combine(notations.date, notations.vstal) - datetime.combine(notations.date,
                                                                                              notations.leg)
        notations.spal = delta_spal.seconds / 60 - notations.nespal
        notations.vkrovati = delta_vkrovati.seconds / 60

        try:
            db.session.commit()
            return redirect('/sleep')
        except:
            return "При редактировании статьи статьи произошла ошибка"
    # todo измени на elif
    else:
        return render_template("notation_update.html", notations=notations)


@app.route('/sleep', methods=['POST', 'GET'])
def add_notation():
    if request.method == "POST":
        date = str_to_ymd(request.form['date'])
        leg = str_to_time(request.form['leg'])
        usnul = str_to_time(request.form['usnul'])
        prosnul = str_to_time(request.form['prosnul'])
        vstal = str_to_time(request.form['vstal'])
        nespal = str_to_time(request.form['nespal']).hour * 60 + str_to_time(request.form['nespal']).minute
        spal = get_timedelta(date, date, prosnul, usnul).seconds / 60 - nespal
        vkrovati = get_timedelta(date, date, vstal, leg).seconds / 60

        # todo отформатировать передавемые параметры(сдалть на разных сроках)
        notation = Notation(date=date, spal=spal, vkrovati=vkrovati, leg=leg, usnul=usnul,
                            prosnul=prosnul, vstal=vstal, nespal=nespal)
        try:
            db.session.add(notation)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении статьи произошла ошибка"
    #     todo измени на elif
    else:
        return render_template('sleep.html')


# todo разбит на несколько функций
@app.route('/edit', methods=['POST', 'GET'])
def edit_dairy():
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
                            elem.date, elem.leg.strftime('%H:%M'), elem.usnul.strftime('%H:%M'),
                            elem.prosnul.strftime('%H:%M'), elem.vstal.strftime('%H:%M'), elem.nespal, elem.spal,
                            elem.vkrovati, eff(elem.spal, elem.vkrovati)
                        ])
                return send_file('../export_dairy.csv')
            except:
                return "При эспортировании произошла ошибка"
        elif request.form.get('import') == 'Импортировать дневник':
            try:
                count = 0
                with open(request.form['importfile'], "r") as file:
                    reader = csv.reader(file)
                    next(reader)
                    for row in reader:
                        date = datetime.date(datetime.strptime(row[0], '%Y-%m-%d'))
                        leg = str_to_time(row[1])
                        usnul = str_to_time(row[2])
                        prosnul = str_to_time(row[3])
                        vstal = str_to_time(row[4])
                        nespal = int(row[5])
                        spal = get_timedelta(date, date, prosnul, usnul).seconds / 60 - nespal
                        vkrovati = get_timedelta(date, date, vstal, leg).seconds / 60

                        notation = Notation(date=date, spal=spal, vkrovati=vkrovati, leg=leg, usnul=usnul,
                                            prosnul=prosnul, vstal=vstal, nespal=nespal)
                        try:
                            db.session.add(notation)
                            db.session.commit()
                            count += 1
                        except:
                            return "При добавлении статьи произошла ошибка"
                return f"Успешно импортировано записей: {count}"
            except:
                return "При импортировании произошла ошибка"

        elif request.form.get('deletedairy') == 'Удалить дневник':
            try:
                db.session.query(Notation).delete()
                db.session.commit()
                return 'Все записи успешно удалены'
            except:
                return 'При удалении записей произошла ошибка'
    #     todo elif
    else:
        return render_template("edit_dairy.html")


@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html")
