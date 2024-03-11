from datetime import datetime

import sqlalchemy.exc
from flask import render_template, redirect, url_for
from flask_login import login_required

from app.controller import *
from app.exceptions.exception import *


# request

@login_required
def create_and_save_entry():
    try:
        # logger
        new_entry = DiaryEntryManager().create_entry()
        add_and_commit(new_entry)
        flash('Новая запись добавлена в дневник сна')
    except sqlalchemy.exc.IntegrityError as err:
        flash(f'Запись с датой "{err.params[0]}" уже существует.')
    except ValueError as err:
        flash(f"{err.args[0]}")
    except Exception as err:
        display_unknown_error(err)
    finally:
        # logger
        return redirect(url_for('get_sleep_diary_entries'))


@login_required
def render_sleep_diary_page():
    """Отображает все записи дневника сна из БД"""
    try:
        # logger
        diary_entries = DiaryEntryManager().diary_entries()
        statistics = DiaryEntryManager().weekly_statistics(diary_entries)
        return render_template(
            "sleep.html",
            today_date=datetime.date(datetime.today()),
            enumerate=enumerate,
            diary_entries=diary_entries,
            amount_diary_entries=len(diary_entries),
            statistics=statistics
        )
    except Exception as err:
        display_unknown_error(err)
        return redirect(url_for('get_main_page'))
    # finally:
    # logger
