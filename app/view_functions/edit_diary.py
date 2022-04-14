from flask import flash, request, render_template
from flask_login import login_required

from app.controller import *

# todo сделать try/except/finally


@login_required
def render_edit_diary_page():
    return render_template("edit_diary.html")


@login_required
def diary_editing_actions():
    if request.form.get('export') == 'Экспортировать дневник':
        return export_diary()
    elif request.form.get('import') == 'Импортировать дневник':
        f = request.files['importfile']
        f.save('import_file.csv')
        return import_diary()
    elif request.form.get('delete_diary_1') == 'Удалить дневник':
        flash('Вы действительно хотите удалить все записи из дневника сна?')
        return render_template("edit_diary.html", request_delete_all_notations=True)
    elif request.form.get('delete_diary_2') == 'Да, удалить все записи из дневника':
        return delete_diary()
