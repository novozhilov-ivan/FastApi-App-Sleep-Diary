from app import app
from app.view_functions import render_main_page


@app.route('/')
@app.route('/main')
def get_main_page():
    """Отображает сформированную основную страницу"""
    return render_main_page()
