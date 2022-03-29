from flask import render_template, g
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import app
from .config import login_manager
from .functions import *
from .models import User, db
from .exception import SleepLessTimeInBedError


# todo доработать возникновение исключения - при времени сна больше времени в кровати

# todo в импорт дневника добавить проверку перед добавлением данных из файла.
#  Если дата записи из файла имеется в бд, то указать какие даты повторяются и попросить пользователя их исправить
#  и импортировать еще раз

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
    return User.query.get(user_id)


@app.route('/user_page', methods=['POST', 'GET'])
@login_required
def get_user_page():
    """Вызывается с кнопки 'User'. Открывает страницу пользователя, если он авторизован,
    иначе переадресовывает на страницу логин"""
    if request.method == 'POST':
        sign_out()
        return redirect(url_for('sign_in'))
    elif request.method == 'GET':
        return render_template('user_page.html')


@app.route('/login', methods=['POST', 'GET'])
def sign_in():
    """Форма авторизации пользователя"""
    if current_user.is_authenticated:
        return redirect(url_for('get_user_page'))

    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if login and password:
            user = User.query.filter_by(login=login).first()
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
                db.session.add(new_user)
                db.session.commit()
                flash(f"Пользователь '{login}' успешно создан.")
                return redirect(url_for('get_user_page'))
            except sqlalchemy.exc.IntegrityError:
                flash(f"Пользователь '{login}' уже существует. Придумайте уникальное имя пользователя.")
            except (Exception,):
                flash('Ошибка создания пользователя в БД.')
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


@app.route('/sleep', methods=['POST', 'GET'])
@login_required
def sleep_diary():
    """Отображает все записи дневника сна из БД;
    Добавляет одну запись в БД, используя данные из формы"""
    if request.method == "POST":
        calendar_date = str_to_date(request.form.get('calendar_date'))
        bedtime = str_to_time(request.form['bedtime'])
        asleep = str_to_time(request.form['asleep'])
        awake = str_to_time(request.form['awake'])
        rise = str_to_time(request.form['rise'])
        without_sleep = str_to_time(request.form['without_sleep'])
        without_sleep = without_sleep.hour * 60 + without_sleep.minute
        sleep_duration = get_timedelta(calendar_date, awake, asleep).seconds / 60 - without_sleep
        time_in_bed = get_timedelta(calendar_date, rise, bedtime).seconds / 60
        user_id = current_user.id

        notation = Notation(
            calendar_date=calendar_date, sleep_duration=sleep_duration, time_in_bed=time_in_bed,
            bedtime=bedtime, asleep=asleep, awake=awake, rise=rise, without_sleep=without_sleep,
            user_id=user_id
        )
        try:
            if time_in_bed < sleep_duration:
                raise SleepLessTimeInBedError
            db.session.add(notation)
            db.session.commit()
            flash('Новая запись успешно добавлена в дневник сна')
        except sqlalchemy.exc.IntegrityError:
            flash('При добавлении записи в произошла ошибка.')
            flash(f'Запись с датой "{calendar_date}" уже существует.')
        except SleepLessTimeInBedError:
            flash('Ошибка данных. Время проведенное в кровати не может быть меньше времени сна.')
        except (Exception,) as err:
            flash(f'При добавлении записи произошла ошибка. Прочая ошибка. {err}')
        finally:
            return redirect(url_for('sleep_diary'))

    elif request.method == "GET":
        all_notations = db.session.query(Notation).order_by(Notation.calendar_date).filter_by(user_id=current_user.id)
        db_notation_counter = db.session.query(Notation).count()
        return render_template(
            "sleep.html", all_notations=all_notations, time_display=time_display,
            average_sleep_duration_per_week=get_average_sleep_duration_per_week,
            sleep_efficiency=sleep_efficiency, db_notation_counter=db_notation_counter,
            average_sleep_efficiency_per_week=get_average_sleep_efficiency_per_week,
            check_notations=get_amount_notations_of_week, today_date=today_date,
            enumerate=enumerate
        )


@app.route('/sleep/update/<notation_date>', methods=['POST', 'GET'])
@login_required
def edit_notation(notation_date):
    """Редактирование одной записи в дневнике. Удаление всей записи/изменения времени в формах"""
    try:
        notation = db.session.query(Notation).filter_by(user_id=current_user.id, calendar_date=notation_date).first()
    except ValueError:
        flash(f'Записи с датой {notation_date} не существует')
        return redirect(url_for('sleep_diary'))
    except (Exception,):
        flash('При загрузки страницы редактирования произошла ошибка')
        return redirect(url_for('sleep_diary'))
    else:
        if request.method == "POST":
            if request.form.get('update_save') == 'Сохранить изменения':
                return edit_notation_update(notation_date)
            elif request.form.get('delete_notation_1') == 'Удалить запись':
                flash(f'Вы действительно хотите удалить запись {notation_date} из дневника?')
                return render_template(
                    "edit_notation.html", request_delete_notation=True,
                    notation_date=notation_date, notation=notation
                )
            elif request.form.get('delete_notation_2') == 'Да, удалить запись из дневника':
                return delete_notation(notation_date)
        elif request.method == "GET":
            return render_template("edit_notation.html", notation=notation)


@app.route('/edit', methods=['POST', 'GET'])
@login_required
def edit_diary():
    """Вызов функций редактирование дневника сна: экспорт, импорт и удаление всех записей"""
    if request.method == 'POST':
        if request.form.get('export') == 'Экспортировать дневник':
            return edit_diary_export()
        elif request.form.get('import') == 'Импортировать дневник':
            f = request.files['importfile']
            f.save('import_file.csv')
            return edit_diary_import()
        elif request.form.get('delete_diary_1') == 'Удалить дневник':
            flash('Вы действительно хотите удалить все записи из дневника сна?')
            return render_template("edit_diary.html", request_delete_all_notations=True)
        elif request.form.get('delete_diary_2') == 'Да, удалить все записи из дневника':
            return edit_diary_delete_all_notations()
    elif request.method == "GET":
        return render_template("edit_diary.html")


@app.route('/')
@app.route('/main')
def main():
    """Открывает начальную страницу"""
    return render_template("main.html")
