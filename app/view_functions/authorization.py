import sqlalchemy.exc
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.config import mode
from app.controller import *
from app.model import *


def authorize():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = check_user(login)
        if user and check_password_hash(user.password, password):
            remain = True if request.form.get('remain') else False
            login_user(user, remember=remain)
            flash(f"Вы успешно вошли на аккаунт {user.login}")
            try:
                return redirect(request.args.get("next"))
            except AttributeError:
                return redirect(url_for('get_user_page'))
        flash('Неверное имя пользователя или пароль')
        return redirect(url_for('render_login_page'))
    flash('Пожалуйста заполните поля логин и пароль')
    return render_template("login.html")


@login_required
def deauthorize():
    try:
        logout_user()
        return redirect(url_for('sign_in'))
    except Exception as err:
        flash(err.args[0])
        return redirect(url_for('get_user_page'))


def register():
    try:
        login = request.form.get('login')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if not (login or password1 or password2):
            raise ValueError('Пожалуйста заполните все поля.')
        elif password2 != password1:
            raise ValueError('Пароли должны быть одинаковые.')
        else:
            hash_password = generate_password_hash(password1)
            new_user = User()
            new_user.login, new_user.password = login, hash_password
            # todo Этим try-except должен заняться менеджер при создании нового пользователя
            # todo При ошибке - возбуждать исключение, а его текст будет отображаться уже в try-except здесь
            # todo в первый обработчик ошибок ВНЕСТИ ВСЕ ТИПЫ, которые мне известны, а ниже неизвестные;
            # todo неизвестные будут отображаться в prod как 'прочая ошибка', а в dev выводиться
            try:
                add_and_commit(new_user)
                flash(f"Пользователь '{login}' успешно создан.")
                return redirect(url_for('get_user_page'))
            except sqlalchemy.exc.IntegrityError:
                flash(f"Имя пользователя {login} уже занято. Придумайте уникальное имя пользователя.")
                return redirect(url_for('registration'))
            except Exception as err:
                flash(f'Ошибка создания пользователя в БД. {err}')
                return redirect(url_for('registration'))
    except (ValueError, ) as err:
        flash(err.args[0])
        return redirect(url_for('registration'))
    except Exception as err:
        flash(err.args[0] if mode else 'Неизвестная ошибка')
        return redirect(url_for('registration'))


@login_required
def render_user_page():
    return render_template('user_page.html', date_and_time_display=date_and_time_display,
                           amount_notations_of_user=get_amount_notations_of_user())


def render_login_page():
    if current_user.is_authenticated:
        return redirect(url_for('get_user_page'))
    return render_template("login.html")


def render_registration_page():
    return render_template("registration.html")
