from app import app


@app.route('/user_page', methods=['POST'])
def get_user_page():
    """Вызывается с кнопки 'User'. Открывает страницу пользователя, если он авторизован,
    иначе переадресовывает на страницу логин"""
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


@app.route('/logout', methods=['POST'])
def sign_out():
    """Де авторизация пользователя"""
    return do_sign_out()


@app.route('/logout', methods=['GET'])
def get_sign_out_page():
    return render_sidn_out_page()
