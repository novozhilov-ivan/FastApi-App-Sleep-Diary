from flask import render_template, request, redirect, url_for, flash

from app.controller import *


# notation = Notation.add_notation_and_commit(
#     request.form.form['calendar_date'],
#     request.form['bedtime'],
#     request.form['asleep'],
#     request.form['awake'],
#     request.form['rise'],
#     request.form['without_sleep']
# )

class Manager:

    def get_sleep_diary(self):
        all_notations_of_user = get_all_notations_of_user()
        return render_template(
            "sleep.html", time_display=time_display, all_notations=all_notations_of_user,
            average_sleep_duration_per_week=get_average_sleep_duration_per_week,
            sleep_efficiency=sleep_efficiency, amount_notations_of_user=len(all_notations_of_user),
            average_sleep_efficiency_per_week=get_average_sleep_efficiency_per_week,
            get_amount_notations_of_week=get_amount_notations_of_week,
            today_date=today_date, enumerate=enumerate
        )
