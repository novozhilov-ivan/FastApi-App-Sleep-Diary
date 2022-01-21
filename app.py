from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sleepdairy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Notation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    week = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    leg = db.Column(db.Time, nullable=False)
    usnul = db.Column(db.Time, nullable=False)
    prosnul = db.Column(db.Time, nullable=False)
    vstal = db.Column(db.Time, nullable=False)
    nespal = db.Column(db.INT, nullable=False)
    spal = db.Column(db.INT, nullable=False)
    vkrovati = db.Column(db.INT, nullable=False)

    def __repr__(self):
        return '<Notation %r>' % self.id


def str_to_time(self):
    return datetime.time(datetime.strptime(self, '%H:%M'))


def str_to_ymd(self):
    return datetime.date(datetime.strptime(self, '%Y-%m-%d'))


def timedelta_to_minutes(self):
    return self.seconds / 60


@app.route('/sleep')
def sleep():
    def h_m(self):
        if type(self) == int:
            hm = str(self // 60) + ':' + str(self % 60)
        else:
            hm = self.strftime('%H:%M')
        return hm

    def eff(spal, nespal, vkrovati):
        return round(((spal - nespal) / vkrovati * 100), 2)

    notations = Notation.query.order_by(Notation.date.desc()).all()
    return render_template("sleep.html", notations=notations, h_m=h_m, eff=eff)


@app.route('/sleep', methods=['POST', 'GET'])
def add_notation():
    if request.method == "POST":
        date = str_to_ymd(request.form['date'])
        week = request.form['week']
        day = request.form['day']
        leg = str_to_time(request.form['leg'])
        usnul = str_to_time(request.form['usnul'])
        prosnul = str_to_time(request.form['prosnul'])
        vstal = str_to_time(request.form['vstal'])
        nespal = str_to_time(request.form['nespal']).hour * 60 + str_to_time(request.form['nespal']).minute

        delta_spal = datetime.combine(date, prosnul) - datetime.combine(date, usnul)
        delta_vkrovati = datetime.combine(date, vstal) - datetime.combine(date, leg)

        spal = timedelta_to_minutes(delta_spal) - nespal
        vkrovati = timedelta_to_minutes(delta_vkrovati)

        notation = Notation(date=date, week=week, day=day, spal=spal, vkrovati=vkrovati, leg=leg, usnul=usnul,
                            prosnul=prosnul, vstal=vstal, nespal=nespal)
        try:
            db.session.add(notation)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('sleep.html')


@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/data_form')
def data():
    return render_template("data-form.html")


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')


@app.route('/support')
def support():
    return render_template('support.html')


if __name__ == "__main__":
    app.run(debug=True)
