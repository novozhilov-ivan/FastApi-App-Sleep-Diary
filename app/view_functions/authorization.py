import sqlalchemy.exc
from app.Models import *
from app.exceptions.exception import *
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.controller import *


def authorize():
    try:
        # logger
        login = request.form.get("sign_in")
        password = request.form.get("password")
        if login and password:
            user = check_user(login)
            if user and check_password_hash(user.password, password):
                remain = True if request.form.get("remain") else False
                login_user(user, remember=remain)
                flash(f"Вы успешно вошли на аккаунт {user.login}")
                try:
                    return redirect(request.args.get("next"))
                except AttributeError:
                    return redirect(url_for("get_user_page"))
            flash("Неверное имя пользователя или пароль")
            return redirect(url_for("render_login_page"))
        flash("Пожалуйста заполните поля логин и пароль")
        return render_template("sign_in.html")
    except Exception as err:
        flash(
            f"Ошибка при проверке пользователя в базе данных. Прочая ошибка. "
            f"{err.args[0]}"
        )
        return render_template("sign_in.html")
    # except:
    # TODO сделать проверку на наличие пользователя в бд. Добавить соответсвующий
    #  флеш при отсутствии пользователя.
    # finally:
    # logger


@login_required
def deauthorize():
    try:
        # logger
        logout_user()
        return redirect(url_for("sign_in"))
    except Exception as err:
        flash(
            f"Ошибка при проверке пользователя в базе данных. Прочая ошибка. "
            f"{err.args[0]}"
        )
        return redirect(url_for("get_user_page"))
    # finally:
    # logger


def register():
    try:
        # logger
        login = request.form.get("sign_in")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if not (login or password1 or password2):
            raise ValueError("Пожалуйста заполните все поля.")
        elif password2 != password1:
            raise ValueError("Пароли должны быть одинаковые.")
        else:
            hash_password = generate_password_hash(password1)
            new_user = User()
            new_user.login, new_user.password = login, hash_password
            # todo Этим try-except должен заняться менеджер при создании нового
            #  пользователя
            # todo При ошибке - возбуждать исключение, а его текст будет
            #  отображаться уже в try-except здесь
            # todo в первый обработчик ошибок ВНЕСТИ ВСЕ ТИПЫ, которые мне
            #  известны, а ниже неизвестные;
            # todo неизвестные будут отображаться в prod как 'прочая ошибка',
            #  а в dev выводиться
            add_and_commit(new_user)
    except sqlalchemy.exc.IntegrityError as err:
        flash(
            f'Имя пользователя "{err.params[0]}" уже занято. Придумайте уникальное '
            f"имя пользователя."
        )
    except (ValueError,) as err:
        flash(err.args[0])
    except Exception as err:
        display_unknown_error(err)
    else:
        flash(f"Пользователь '{login}' успешно создан.")
    finally:
        return redirect(url_for("registration"))
        # logger


@login_required
def render_user_page():
    try:
        # logger
        return render_template(
            "user_page.html",
            date_and_time_display=date_and_time_display,
            amount_DreamNotes_of_user=get_amount_DreamNotes_of_user(),
        )
    except Exception as err:
        display_unknown_error(err)
    # finally:
    # logger


def render_login_page():
    try:
        # logger
        if current_user.is_authenticated:
            return redirect(url_for("get_user_page"))
        return render_template("sign_in.html")
    except Exception as err:
        display_unknown_error(err)
    # finally:
    # logger


def render_registration_page():
    try:
        return render_template("registration.html")
    except Exception as err:
        display_unknown_error(err)
    # finally:
    # logger
