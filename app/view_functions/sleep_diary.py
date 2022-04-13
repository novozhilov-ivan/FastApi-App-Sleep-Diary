from datetime import datetime

import sqlalchemy.exc
from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app.controller import *

# todo добавить логирование и занести в try/finally
# todo Добавить мб расчет количества недель через деление и округление вверх. Для jinja(чтобы
# todo

@login_required
def create_and_save_entry():
    try:
        new_entry = DiaryEntryManager().create_entry()
        add_and_commit(new_entry)
        flash('Новая запись добавлена в дневник сна')
    except sqlalchemy.exc.IntegrityError as err:
        flash(f'Запись с датой "{err.params[0]}" уже существует.')
    except ValueError as err:
        flash(f"{err.args[0]}")
    except Exception as err:
        flash(f'При добавлении записи произошла ошибка. Прочая ошибка. {err.args[0]}')
    finally:
        return redirect(url_for('get_sleep_diary_entries'))


@login_required
def render_sleep_diary_page():
    """Отображает все записи дневника сна из БД"""
    try:
        diary_entries = DiaryEntryManager().diary_entries()
        statistics = DiaryEntryManager().statistics(diary_entries)
        return render_template(
            "sleep.html",
            today_date=datetime.date(datetime.today()),
            enumerate=enumerate,
            diary_entries=diary_entries,
            amount_diary_entries=len(diary_entries),
            statistics=statistics
        )
    except Exception as err:
        flash(f'При получении страницы произошла ошибка. Прочая ошибка. {err.args[0]}')
        return redirect(url_for('get_main_page'))
