import sqlalchemy.exc
from flask import flash, request, render_template, redirect, url_for
from flask_login import login_required

from app import db
from app.controller import *
from app.exception import display_unknown_error


@login_required
def update_one_diary_entry(notation_date):
    try:
        # logger
        notation = get_notation_by_date(notation_date)
        entry = DiaryEntryManager()
        if request.form.get('update_save') == 'Сохранить изменения':
            entry.update_entry(notation)
            db.session.commit()
            flash(f'Запись {notation_date} обновлена.')
            return redirect(url_for('get_sleep_diary_entries'))
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
            flash(f'Запись {notation_date} удалена.')
            return redirect(url_for('get_sleep_diary_entries'))
    except KeyError as err:
        flash(err.args[0])
        return redirect(f'/sleep/update/{notation_date}')
    except (ValueError, TypeError) as err:
        flash(err.args[0])
        return redirect(f'/sleep/update/{notation_date}')
    except Exception as err:
        display_unknown_error(err)
        return redirect(f'/sleep/update/{notation_date}')
    # finally:
        # logger
# flash(f'При удалении записи {notation.calendar_date} произошла ошибка.')
#


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
        return redirect(f'/sleep/update/{notation_date}')
    else:
        return render_template(
            "edit_notation.html",
            notation=notation
        )
    # finally:
        # logger
