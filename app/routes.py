from flask import render_template
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import app
from .functions import *
from .models import User, db
from .config import login_manager


# todo настроить куки
# todo настроить отображение данных отдельно для каждого пользователя
# todo переделать бд, сделать отдельную колонку, которая обозначает очередь записи согласно дате записи для уникального
#  пользователя; колонку id сделать первичным ключом, а у даты забрать;
#  todo Колонка с номером очереди записи должна быть уникальной для каждого пользователя


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
        return render_template('user_page.html', signout=sign_out())


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
            else:
                flash('Неверное имя пользователя или пароль')
                return render_template("login.html")
        else:
            flash('Пожалуйста заполните поля логин и пароль')
            return render_template("login.html")
    elif request.method == 'GET':
        return render_template("login.html")
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
            new_user = User(login=login, password=hash_password)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash(f"Пользователь с именем '{login}' успешно создан.")
                return redirect(url_for('get_user_page'))
            except sqlalchemy.exc.IntegrityError:
                flash(f"Пользователь '{login}' уже существует. Придумайте уникальное имя пользователя.")
            except (Exception, ):
                flash('Ошибка создания пользователя в БД.')
                return redirect(url_for('registration'))
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

        notation = Notation(calendar_date=calendar_date, sleep_duration=sleep_duration, time_in_bed=time_in_bed,
                            bedtime=bedtime, asleep=asleep, awake=awake, rise=rise, without_sleep=without_sleep,
                            user_id=user_id)
        # try:
        db.session.add(notation)
        id_notations_update()
        flash('Новая запись успешно добавлена в дневник сна')
        return redirect(url_for('sleep_diary'))
        # except sqlalchemy.exc.IntegrityError:
        #     flash("При добавлении записи в базу данных произошла ошибка. Дата записи должна быть уникальной.")
        #     return redirect(url_for('sleep_diary'))
        # except (Exception,):
        #     flash('При добавлении записи в базу данных произошла ошибка. Прочая ошибка.')
        #     return redirect(url_for('sleep_diary'))
    elif request.method == "GET":
        all_notations = db.session.query(Notation).order_by(Notation.calendar_date).all()
        db_notation_counter = db.session.query(Notation).count()

        def average_sleep_efficiency_per_week(week_number):
            """Вычисляет среднюю эффективность сна за неделю"""
            sum_of_efficiency, week_length = 0, 0
            first_day_of_week = 7 * (week_number - 1) + 1
            last_day_of_week = 8 * week_number - (week_number - 1)
            for day in range(first_day_of_week, last_day_of_week):
                for _notation in all_notations:
                    if _notation.id != day:
                        continue
                    week_length += 1
                    if _notation.sleep_duration != 0:
                        sum_of_efficiency += _notation.sleep_duration / _notation.time_in_bed
            if week_length == 0:
                return 0
            return round(((sum_of_efficiency / week_length) * 100), 2)

        def average_sleep_duration_per_week(week_number):
            """Вычисляет среднюю продолжительность сна за неделю"""
            sum_of_minutes, week_length = 0, 0
            first_day_of_week = 7 * (week_number - 1) + 1
            last_day_of_week = 8 * week_number - (week_number - 1)
            for day in range(first_day_of_week, last_day_of_week):
                for _notation in all_notations:
                    if _notation.id != day:
                        continue
                    week_length += 1
                    sum_of_minutes += _notation.sleep_duration
            if week_length == 0:
                return 0
            return int(sum_of_minutes / week_length)

        def check_notations(week_number):
            """Проверка количества записей в неделе"""
            amount = 0
            first_day_of_week = 7 * (week_number - 1) + 1
            last_day_of_week = 8 * week_number - (week_number - 1)
            for day in range(first_day_of_week, last_day_of_week):
                for _notation in all_notations:
                    if _notation.id != day:
                        continue
                    amount += 1
            if amount == 0:
                return 0
            return amount

        def today_date():
            """Возвращает текущую локальную дату в формате 'YYYY-MM-DD'"""
            return datetime.date(datetime.today())

        return render_template("sleep.html", all_notations=all_notations, time_display=time_display,
                               average_sleep_duration_per_week=average_sleep_duration_per_week,
                               sleep_efficiency=sleep_efficiency, db_notation_counter=db_notation_counter,
                               average_sleep_efficiency_per_week=average_sleep_efficiency_per_week,
                               check_notations=check_notations, today_date=today_date)


@app.route('/sleep/update/<notation_date>', methods=['POST', 'GET'])
@login_required
def edit_notation(notation_date):
    """Редактирование одной записи в дневнике. Удаление всей записи/изменения времени в формах"""
    try:
        notation = Notation.query.get(str_to_date(notation_date))
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
                return render_template("edit_notation.html", request_delete_notation=True, notation_date=notation_date,
                                       notation=notation)
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
