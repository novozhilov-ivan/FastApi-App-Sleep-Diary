import sqlalchemy.exc
from flask import flash, request, render_template, redirect, url_for
from flask_login import login_required

from app.controller import *

# todo сделать try/except/finally


@login_required
def update_one_diary_entry(notation_date):
    notation = get_notation_by_date(notation_date)
    if request.form.get('update_save') == 'Сохранить изменения':
        return update_notation(notation)
    elif request.form.get('delete_notation_1') == 'Удалить запись':
        flash(f'Вы действительно хотите удалить запись {notation_date} из дневника?')
        return render_template(
            "edit_notation.html", request_delete_notation=True,
            notation_date=notation_date, notation=notation
        )
    elif request.form.get('delete_notation_2') == 'Да, удалить запись из дневника':
        return delete_notation(notation)


@login_required
def render_diary_entry_update_page(notation_date):
    try:
        notation = get_notation_by_date(notation_date)
    except sqlalchemy.exc.NoResultFound:
        flash(f'Записи с датой {notation_date} не существует.')
        return redirect(url_for('get_sleep_diary_entries'))
    except (Exception,):
        flash(f'При загрузки страницы редактирования произошла ошибка..')
        return redirect(url_for('get_sleep_diary_entries'))
    else:
        return render_template("edit_notation.html", notation=notation)
