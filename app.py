from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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
    nespal = db.Column(db.Time, nullable=False)

    # def __repr__(self):
    #     return '<Notation %r>' % self.id


def strtotime(self):
    return datetime.time(datetime.strptime(self, "%H:%M"))


def strtoymd(self):
    return datetime.date(datetime.strptime(self, "%Y-%m-%d"))


@app.route('/sleep')
def sleep():
    notations = Notation.query.order_by(Notation.date.desc()).all()
    return render_template("sleep.html", notations=notations)


@app.route('/sleep', methods=['POST', 'GET'])
def addnotation():
    if request.method == "POST":
        date = strtoymd(request.form['date'])
        week = request.form['week']
        day = request.form['day']
        leg = strtotime(request.form['leg'])
        usnul = strtotime(request.form['usnul'])
        prosnul = strtotime(request.form['prosnul'])
        vstal = strtotime(request.form['vstal'])
        nespal = strtotime(request.form['nespal'])

        notation = Notation(date=date, week=week, day=day, leg=leg, usnul=usnul, prosnul=prosnul, vstal=vstal,
                            nespal=nespal)
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
