import sqlalchemy.exc
from app.exceptions.exception import display_unknown_error
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.controller import *


@login_required
def update_one_diary_entry(SleepDiaryEntry_date):
    try:
        # logger
        if request.form.get("update_save") == "Сохранить изменения":
            DiaryEntryManager().update_entry(SleepDiaryEntry_date)
            flash(f'Запись "{SleepDiaryEntry_date}" обновлена.')
        elif request.form.get("delete_SleepDiaryEntry_1") == "Удалить запись":
            flash(
                f"Вы действительно хотите удалить запись {SleepDiaryEntry_date} из "
                f"дневника?"
            )
        elif (
            request.form.get("delete_SleepDiaryEntry_2")
            == "Да, удалить запись из дневника"
        ):
            DiaryEntryManager().delete_entry(SleepDiaryEntry_date)
            flash(f'Запись "{SleepDiaryEntry_date}" удалена.')
    except KeyError as err:
        flash(err.args[0])
    except (ValueError, TypeError) as err:
        flash(err.args[0])
    except Exception as err:
        display_unknown_error(err)
    finally:
        # logger
        if request.form.get("delete_SleepDiaryEntry_1") == "Удалить запись":
            return render_template(
                "edit_SleepDiaryEntry.html",
                confirm_delete_SleepDiaryEntry=True,
                SleepDiaryEntry=get_SleepDiaryEntry_by_date(SleepDiaryEntry_date),
            )
        elif (
            request.form.get("update_save") == "Сохранить изменения"
            or request.form.get("delete_SleepDiaryEntry_2")
            == "Да, удалить запись из дневника"
        ):
            return redirect(url_for("get_sleep_diary_entries"))
        else:
            return redirect(f"/sleep/update/{SleepDiaryEntry_date}")


@login_required
def render_diary_entry_update_page(SleepDiaryEntry_date):
    try:
        # logger
        SleepDiaryEntry = get_SleepDiaryEntry_by_date(SleepDiaryEntry_date)
    except sqlalchemy.exc.NoResultFound:
        flash(f'Записи с датой "{SleepDiaryEntry_date}" не существует.')
        return redirect(url_for("get_sleep_diary_entries"))
    except Exception as err:
        display_unknown_error(err)
        return redirect(url_for("get_sleep_diary_entries"))
    else:
        return render_template(
            "edit_SleepDiaryEntry.html", SleepDiaryEntry=SleepDiaryEntry
        )
    # finally:
    # logger
