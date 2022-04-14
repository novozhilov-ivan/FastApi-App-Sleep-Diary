import sqlalchemy.exc
from flask import flash, request, render_template, redirect, url_for
from flask_login import login_required

from app.controller import *
from app.exception import display_unknown_error
# todo сделать try/except/finally


@login_required
def update_one_diary_entry(notation_date):
    try:
        notation = get_notation_by_date(notation_date.strip('<>'))
        if request.form.get('update_save') == 'Сохранить изменения':
            return update_notation(notation)
        elif request.form.get('delete_notation_1') == 'Удалить запись':
            flash(f'Вы действительно хотите удалить запись {notation_date} из дневника?')
            return render_template(
                "edit_notation.html",
                request_delete_notation=True,
                notation_date=notation_date,
                notation=notation
            )
        elif request.form.get('delete_notation_2') == 'Да, удалить запись из дневника':
            delete_notation_and_commit(notation)
            flash(f'Запись {notation.calendar_date} удалена.')
            return redirect(url_for('get_sleep_diary_entries'))
    except Exception as err:
        display_unknown_error(err)
        return redirect(url_for(f'/sleep/update/<{notation.calendar_date}>'))
        # return redirect(url_for('get_sleep_diary_entries'))
    # finally:
        # logger
# flash(f'При удалении записи {notation.calendar_date} произошла ошибка.')
#


@login_required
def render_diary_entry_update_page(notation_date):
    # try:
    # todo Ошибка no result found - хотя запись с такой датой есть
    # todo Проверить какой тип данных у notation date
    notation = get_notation_by_date(notation_date)
    return render_template(
        "edit_notation.html",
        notation=notation
    )
    # except sqlalchemy.exc.NoResultFound as err:
    #     display_unknown_error(err)
    #     flash(f'Записи с датой "{notation_date}" не существует.')
    #     return redirect(url_for('get_sleep_diary_entries'))
    # except Exception as err:
    #     display_unknown_error(err)
    #     return redirect(url_for('get_sleep_diary_entries'))
    # finally:
        # logger
