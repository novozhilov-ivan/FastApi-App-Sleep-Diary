import sqlalchemy.exc
from flask import g, render_template

from app import app, login_manager
from app.controller import *
from app.exceptions.exception import *


@app.context_processor
def get_mode():
    """
    Выводит в конце страницы информацию об окружении,
    если FLASK_DEBUG=1 и FLASK_ENV=development;
    Если FLASK_ENV=production и FLASK_DEBUG != 1, то выводит пустую строку"""
    g.flask_env, g.flask_debug = '', ''
    if app.config['FLASK_ENV'] != "production" or app.config['FLASK_DEBUG'] == '1':
        g.flask_env = f"Environment: {app.config['FLASK_ENV']}"
        g.flask_debug = f"Debug mode: {app.config['FLASK_DEBUG']}"
    return dict(
        flask_env=g.flask_env,
        flask_debug=g.flask_debug
    )


@login_manager.user_loader
def load_user(user_id):
    try:
        # logger
        return get_user(user_id)
    except sqlalchemy.exc.ProgrammingError as err:
        return flash('Таблица с пользователями не создана.'), flash(err.args[0])
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
        return display_unknown_error(err)
    # finally:
#         logger
