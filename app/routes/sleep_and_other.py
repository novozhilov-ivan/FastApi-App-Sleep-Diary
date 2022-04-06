from app import app


# todo из .queries переметить все в .models
# todo создать в controller .manager и там class Manager(), который будет получать, переваривать, сохранять данные
#  в соответствующем методе. По такому же принципу добавить методы.


# todo переместить все проверки, изменение формата и создание записи в дневнике -
#  в класс Notation (например сделать  Notation.add_notation(*args))

# todo пофиксить ошибку пустых полей в регистрации
# todo пофиксить регистрацию нового пользователя без пароля

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


@app.route('/')
@app.route('/main')
def get_main_page():
    """Отображает сформированную основную страницу"""
    return render_main_page()
