import sqlalchemy.exc
from flask import flash, request, render_template, redirect, url_for
from flask_login import login_required

from app.controller import *
from app.exception import display_unknown_error


@login_required
def update_one_diary_entry(notation_date):
    try:
        # logger
        if request.form.get('update_save') == 'Сохранить изменения':
            DiaryEntryManager().update_entry(notation_date)
            flash(f'Запись "{notation_date}" обновлена.')
        elif request.form.get('delete_notation_1') == 'Удалить запись':
            flash(f'Вы действительно хотите удалить запись {notation_date} из дневника?')
        elif request.form.get('delete_notation_2') == 'Да, удалить запись из дневника':
            DiaryEntryManager().delete_entry(notation_date)
            flash(f'Запись "{notation_date}" удалена.')
    except KeyError as err:
        flash(err.args[0])
    except (ValueError, TypeError) as err:
        flash(err.args[0])
    except Exception as err:
        display_unknown_error(err)
    finally:
        # logger
        if request.form.get('delete_notation_1') == 'Удалить запись':
            return render_template(
                "edit_notation.html",
                confirm_delete_notation=True,
                notation=get_notation_by_date(notation_date)
            )
        elif (request.form.get('update_save') == 'Сохранить изменения' or
              request.form.get('delete_notation_2') == 'Да, удалить запись из дневника'):
            return redirect(url_for('get_sleep_diary_entries'))
        else:
            return redirect(f'/sleep/update/{notation_date}')


@login_required
def render_diary_entry_update_page(notation_date):
    try:
        # logger
        notation = get_notation_by_date(notation_date)
    except sqlalchemy.exc.NoResultFound:
        flash(f'Записи с датой "{notation_date}" не существует.')
        return redirect(url_for('get_sleep_diary_entries'))
    except Exception as err:
        display_unknown_error(err)
        return redirect(url_for('get_sleep_diary_entries'))
    else:
        return render_template(
            "edit_notation.html",
            notation=notation
        )
    # finally:
        # logger
