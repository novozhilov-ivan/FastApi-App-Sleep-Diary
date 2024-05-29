import os

import sqlalchemy.exc
from app.exceptions.exception import *
from flask import redirect, render_template, request, send_file, url_for
from flask_login import login_required

from app.controller import *


# todo добавить нотации к ошибкам при плохом импортируемом файле


@login_required
def diary_editing_actions():
    src = "app/static/example/file.csv"
    try:
        # logger
        if request.form.get("export") == "Экспортировать дневник":
            generate_export_file(src)
            return send_file(src)
        elif request.form.get("import") == "Импортировать дневник":
            import_file = request.files["importfile"]
            import_file.save(src)
            duplicate_dates = find_duplicate_dates_in_file(src)
            if duplicate_dates:
                raise NonUniqueDreamNoteDate(
                    f'В файле "{import_file.filename}" найдены записи с датами, '
                    f"которые уже существуют в дневнике: "
                    f'"{", ".join(duplicate_dates)}"'
                )
            added_entries = import_diary(src)
            flash(f"Успешно импортировано {len(added_entries)} записей.")
            return redirect(url_for("get_edit_diary_page"))
        elif request.form.get("delete_diary_1") == "Удалить дневник":
            flash("Вы действительно хотите удалить все записи из дневника сна?")
        elif (
            request.form.get("delete_diary_2")
            == "Да, удалить все записи из дневника"
        ):
            delete_all_DreamNotes()
            flash("Все записи из дневника сна удалены.")
    except sqlalchemy.exc.IntegrityError:
        flash(
            "Ошибка при добавлении записей в базу данных. Даты записей должны быть "
            "уникальными."
        )
    except NonUniqueDreamNoteDate as err:
        flash(err.args[0])
    except TypeError as err:
        flash(err.args[0])
    except ValueError as err:
        flash(err.args[0])
    except SyntaxError as err:
        flash(err.args[0])
    except FileNotFoundError as err:
        flash(err.args[0])
    except NameError as err:
        display_unknown_error(err)
    except StopIteration:
        flash("Выберите csv-файл для импорта записей в дневник сна.")
    except Exception as err:
        display_unknown_error(err)
    else:
        if request.form.get("export") == "Экспортировать дневник":
            return redirect(url_for("get_edit_diary_page"))
    finally:
        if os.path.isfile(src):
            os.remove(src)
        if request.form.get("import") == "Импортировать дневник":
            return redirect(url_for("get_edit_diary_page"))
        elif request.form.get("delete_diary_1") == "Удалить дневник":
            return render_template(
                "edit_diary.html", confirm_delete_all_DreamNotes=True
            )
        elif (
            request.form.get("delete_diary_2")
            == "Да, удалить все записи из дневника"
        ):
            return redirect(url_for("get_edit_diary_page"))
        # logger


@login_required
def render_edit_diary_page():
    try:
        # logger
        return render_template("edit_diary.html")
    except Exception as err:
        display_unknown_error(err)
        return redirect(url_for("get_main_page"))
    # finally:
    # logger
