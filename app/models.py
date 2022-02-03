import os
from app import app, db


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sleepdairy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


APP_MODE = os.getenv('FLASK_ENV')


# todo вынести в отдельный модуль
class Notation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    # todo rename var
    leg = db.Column(db.Time, nullable=False)
    usnul = db.Column(db.Time, nullable=False)
    prosnul = db.Column(db.Time, nullable=False)
    vstal = db.Column(db.Time, nullable=False)
    nespal = db.Column(db.INT, nullable=False)
    spal = db.Column(db.INT, nullable=False)
    vkrovati = db.Column(db.INT, nullable=False)

    def __repr__(self):
        return '<Notation %r>' % self.id
