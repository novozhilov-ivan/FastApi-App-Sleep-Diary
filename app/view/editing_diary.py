import sqlalchemy.exc

from flask import flash, request, render_template, redirect, url_for
from flask_login import login_required

from app import app
from app.controller import *


@app.route('/sleep/update/<notation_date>', methods=['POST', 'GET'])
@login_required
def edit_notation(notation_date):
    """Редактирование одной записи в дневнике. Удаление всей записи/изменения времени в формах"""
    try:
        notation = get_notation_by_date(notation_date)
    except sqlalchemy.exc.NoResultFound:
        flash(f'Записи с датой {notation_date} не существует.')
        return redirect(url_for('sleep_diary'))
    except (Exception,):
        flash(f'При загрузки страницы редактирования произошла ошибка..')
        return redirect(url_for('sleep_diary'))
    else:
        if request.method == "POST":
            if request.form.get('update_save') == 'Сохранить изменения':
                return update_notation(notation)

            elif request.form.get('delete_notation_1') == 'Удалить запись':
                flash(f'Вы действительно хотите удалить запись {notation_date} из дневника?')
                return render_template("edit_notation.html", request_delete_notation=True,
                                       notation_date=notation_date, notation=notation
                                       )

            elif request.form.get('delete_notation_2') == 'Да, удалить запись из дневника':
                return delete_notation(notation)

        elif request.method == "GET":
            return render_template("edit_notation.html", notation=notation)


@app.route('/edit', methods=['POST', 'GET'])
@login_required
def edit_diary():
    """Вызов функций редактирование дневника сна: экспорт, импорт и удаление всех записей"""
    if request.method == 'POST':
        if request.form.get('export') == 'Экспортировать дневник':
            return export_diary()
        elif request.form.get('import') == 'Импортировать дневник':
            f = request.files['importfile']
            f.save('import_file.csv')
            return import_diary()
        elif request.form.get('delete_diary_1') == 'Удалить дневник':
            flash('Вы действительно хотите удалить все записи из дневника сна?')
            return render_template("edit_diary.html", request_delete_all_notations=True)
        elif request.form.get('delete_diary_2') == 'Да, удалить все записи из дневника':
            return delete_diary()
    elif request.method == "GET":
        return render_template("edit_diary.html")
