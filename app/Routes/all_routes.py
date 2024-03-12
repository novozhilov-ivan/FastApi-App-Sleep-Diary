from app import app
from app.view_functions import *

# todo из .queries переметить все в .Models
# todo переместить все проверки, изменение формата и создание записи в дневнике -
#  в класс Notation (например сделать  Notation.add_notation(*args))

# todo прикрутить визуализацию данных на гистограммах

# todo сделать unit тесты


@app.route('/sleep', methods=['POST'])
def post_sleep_dairy_entry():
    """Добавляет одну запись в дневник сна/БД"""
    return create_and_save_entry()


@app.route('/sleep', methods=['GET'])
def get_sleep_diary_entries():
    """Получает страницу со всеми записями дневника сна и формирует статистику на основе записей"""
    return render_sleep_diary_page()


@app.route('/sleep/update/<notation_date>', methods=['POST'])
def update_diary_entry(notation_date):
    """Обновляет одну запись в дневнике сна. Удаляет или изменяет"""
    return update_one_diary_entry(notation_date)


@app.route('/sleep/update/<notation_date>', methods=['GET'])
def get_diary_entry_update_page(notation_date):
    return render_diary_entry_update_page(notation_date)


@app.route('/edit', methods=['POST'])
def edit_diary():
    """Вызов функций редактирование дневника сна: экспорт, импорт и удаление всех записей"""
    return diary_editing_actions()


@app.route('/edit', methods=['GET'])
def get_edit_diary_page():
    return render_edit_diary_page()


@app.route('/user_page', methods=['POST'])
def deauthorize_user():
    return deauthorize()


@app.route('/user_page', methods=['GET'])
def get_user_page():
    return render_user_page()


@app.route('/login', methods=['POST'])
def sign_in():
    """Форма авторизации пользователя"""
    return authorize()


@app.route('/login', methods=['GET'])
def get_login_page():
    return render_login_page()



@app.route('/registration', methods=['POST'])
def registration():
    """Регистрация нового пользователя"""
    return register()


@app.route('/registration', methods=['GET'])
def get_registration_page():
    return render_registration_page()
