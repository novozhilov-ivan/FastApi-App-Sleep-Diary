import sqlalchemy.exc

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import app
from app.controller import *
from app.model import *


@app.route('/user_page', methods=['POST', 'GET'])
@login_required
def get_user_page():
    """Вызывается с кнопки 'User'. Открывает страницу пользователя, если он авторизован,
    иначе переадресовывает на страницу логин"""
    if request.method == 'POST':
        sign_out()
        return redirect(url_for('sign_in'))
    elif request.method == 'GET':
        return render_template('user_page.html', date_and_time_display=date_and_time_display,
                               amount_notations_of_user=get_amount_notations_of_user())


@app.route('/login', methods=['POST', 'GET'])
def sign_in():
    """Форма авторизации пользователя"""
    if current_user.is_authenticated:
        return redirect(url_for('get_user_page'))

    if request.method == 'POST':
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
                    return redirect(url_for('sign_in'))
            flash('Неверное имя пользователя или пароль')
            return render_template("login.html")
        flash('Пожалуйста заполните поля логин и пароль')
        return render_template("login.html")
    elif request.method == 'GET':
        return render_template("login.html")


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    """Регистрация нового пользователя"""
    login = request.form.get('login')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not (login or password1 or password2):
            flash('Пожалуйста заполните все поля.')
        elif password2 != password1:
            flash('Пароли должны быть одинаковые.')
        else:
            hash_password = generate_password_hash(password1)
            new_user = User()
            new_user.login, new_user.password = login, hash_password
            try:
                add_and_commit(new_user)
                flash(f"Пользователь '{login}' успешно создан.")
                return redirect(url_for('get_user_page'))
            except sqlalchemy.exc.IntegrityError:
                flash(f"Пользователь '{login}' уже существует. Придумайте уникальное имя пользователя.")
            except (Exception,) as err:
                flash(f'Ошибка создания пользователя в БД. {err}')
                return redirect(url_for('registration'))
    elif request.method == 'GET':
        return render_template("registration.html")


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def sign_out():
    """Де авторизация пользователя"""
    if request.method == "POST":
        logout_user()
        return redirect(url_for('sign_in'))
    elif request.method == "GET":
        return render_template('user_page.html')
