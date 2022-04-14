import os

import sqlalchemy.exc
from flask import g, render_template, flash

from app import app
from app.config import login_manager
from app.controller import *
from app.exception import *


@app.context_processor
def get_mode():
    """Выводит в конце страницы 'development', если включен debug и FLASK_ENV=development;
    Если FLASK_ENV=production, то выводит пустую строку"""
    g.mode = ''
    if os.getenv('FLASK_ENV') != "production":
        g.mode = os.getenv('FLASK_ENV')
    return dict(mode=g.mode)


@login_manager.user_loader
def load_user(user_id):
    try:
        # logger
        return get_user(user_id)
    except sqlalchemy.exc.ProgrammingError as err:
        return flash('Таблица "User" - не создана.'), flash(err.args[0])
    except Exception as err:
        return display_unknown_error(err)
    # finally:
#         logger


def render_main_page():
    """Формирует основную страницу"""
    try:
        # logger
        return render_template('main.html')
    except Exception as err:
        flash(f'Прочая ошибка. {err.args[0]}')
    # finally:
#         logger
