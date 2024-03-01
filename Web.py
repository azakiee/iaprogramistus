from flask import Flask, url_for, render_template, request, redirect, flash, session

app = Flask(__name__)
app.secret_key = "SECRET"

users = [
    {'username': 'Azakie', 'password': '12345'}
]


@app.route('/')
def hello():
    return f"""
    <h1>Мой Сервер</h1>
    <p><a href="{url_for('start')}">Старт</a></p></br>
    <p><a href="{url_for('base')}">База</a></p></br>
    <p><a href="{url_for('form')}">Форма обратной связи</a></p></br>
    <p><a href="{url_for('auth')}">Форма авторизации</a></p></br>
    """


@app.route('/day-<num>')
def day(num):
    return render_template(f'day-{num}.html')


@app.route('/photo-<num>')
def photo(num):
    return render_template(f'photo-{num}.html')


@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        for item in request.form:
            print(f"{item} = {request.form[item]}")
    return render_template('form.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        if session.get("username"):
            return redirect(url_for(f'profile', username=session['username']))
        for user in users:
            if request.form['login'] == user['username']:
                if request.form['password'] == user['password']:
                    flash('Авторизация успешна!')
                    session["username"] = ["username"]
                    return redirect(url_for(f'profile', username=user['username']))

        flash('Неправильный логин или пароль!', category="error")
    return render_template('auth.html')


@app.route('/profile/<username>')
def profile(username):
    return render_template('start.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)