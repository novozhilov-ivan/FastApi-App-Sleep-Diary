import sqlalchemy.exc
from flask import g, render_template

from app import app, login_manager
from app.controller import *
from app.exceptions.exception import *


@login_manager.user_loader
def load_user(user_id):
    try:
        # logger
        return get_user(user_id)
    except sqlalchemy.exc.ProgrammingError as err:
        return flash("Таблица с пользователями не создана."), flash(err.args[0])
    except Exception as err:
        return display_unknown_error(err)
    # finally:


#         logger
