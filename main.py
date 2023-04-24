from flask import Flask, redirect, render_template
from flask_login import login_required, LoginManager, login_user

from app.data.users import User
from forms import AddDateForm, RegistrationForm, LoginForm, Filter

from app.data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main")
        return render_template('authorization.html', message="Wrong data", form=form)
    return render_template('authorization.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        if form.password.data == form.password_again.data:
            user = User(name=form.name.data, surname=form.surname.data, age=form.age.data, email=form.email.data)
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            login_user(user)
            return redirect('/main')
    return render_template('registration.html', title='Sign up', form=form)


@app.route('/')
def func():
    return render_template('base.html', title='Добро пожаловать')


@app.route('/main')
def main():
    param = [["Nastya", "02.03", "anime figure"], ["Julia", "13.07", "candle"], ["Olya", "16.09", "plane ticket"]]
    filter = Filter()
    return render_template('main.html', title='Главная страница', param=param, filter=filter)


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