from flask import Flask, render_template, url_for

app = Flask(__name__)


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
def analytica():
    return render_template('support.html')


if __name__ == "__main__":
    app.run(debug=True)
