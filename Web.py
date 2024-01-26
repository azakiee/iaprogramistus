from flask import Flask, render_template, url_for


app = Flask(__name__)


@app.route("/")
def hello():
    return f"""
    <h1><a href="{url_for('index')}">Сайт</a><h1>
    <h2><a href="{url_for('base')}">База</a><h2>
    <h2><a href="{url_for('start')}">Старт</a><h2>
"""


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/start")
def start():
    return render_template("start.html")


@app.route("/base")
def base():
    return render_template("base.html")


@app.route('/day-<num>')
def day(num):
    return render_template(f'day-{num}.html')


@app.route('/photo-<num>')
def photo(num):
    return render_template(f'photo-{num}.html')


if __name__ == "__main__":
    app.run(debug=True)