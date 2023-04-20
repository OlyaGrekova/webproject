from flask import Flask, redirect, render_template
from flask_login import login_required
from forms import AddDateForm, RegistrationForm, LoginForm

from app.data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('authorization.html', title='Авторизация', form=form)


@app.route('/main')
@login_required
def main():
    pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/birthday/<int:id>', methods=['GET', 'POST'])
@login_required
def birthday(id):
    pass


@app.route('/birthday/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def birthday_edit(id):
    pass


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddDateForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('add_date.html', title='Добавление даты', form=form)


if __name__ == '__main__':
    db_session.global_init("app/db/base.db")
    app.run(port=8081, host='127.0.0.1')