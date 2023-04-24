from flask import Flask, redirect, render_template
from flask_login import login_required
from forms import AddDateForm, RegistrationForm, LoginForm, Filter

from app.data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def func():
    return render_template('base.html', title='Добро пожаловать')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/main')
    return render_template('authorization.html', title='Авторизация', form=form)


@app.route('/main')
def main():
    param = [["Nastya", "02.03", "anime figure"], ["Julia", "13.07", "candle"], ["Olya", "16.09", "plane ticket"]]
    filter = Filter()
    return render_template('main.html', title='Главная страница', param=param, filter=filter)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect('/main')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddDateForm()
    if form.validate_on_submit():
        return redirect('/main')
    return render_template('add_date.html', title='Добавление даты', form=form)



@app.route('/birthday/<int:id>', methods=['GET', 'POST'])
@login_required
def birthday(id):
    pass


@app.route('/birthday/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def birthday_edit(id):
    pass


if __name__ == '__main__':
    db_session.global_init("app/db/base.db")
    app.run(port=8081, host='127.0.0.1')