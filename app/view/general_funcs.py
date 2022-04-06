import os

import sqlalchemy.exc
from flask import g, render_template, flash

from app import app
from app.config import login_manager
from app.controller import *


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
        return get_user(user_id)
    except sqlalchemy.exc.ProgrammingError as err:
        return flash('Таблица "User" - не создана.'), flash(err.args[0])
    except Exception as err:
        return flash('Ошибка при проверке пользователя в базе данных. Прочая ошибка.'), flash(err.args[0])


def render_main_page():
    """Формирует основную страницу"""
    return render_template('main.html')
