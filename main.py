from flask import Flask, redirect, render_template
from flask_login import login_required, LoginManager, login_user
import datetime as dt

from app.data.birthdays import Birthday
from app.data.users import User
from forms import RegistrationForm, LoginForm, Filter, BirthdayForm

from app.data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

id = None
name = 'Юля'
date = '.'.join('13.07.2007'.split('.')[:-1]) + '.' + str((dt.datetime.now().date())).split('-')[0]
now = str((dt.datetime.now().date())).split('-')
left = str(dt.date(int(date.split('.')[2]), int(date.split('.')[1]), int(date.split('.')[0])) - dt.date(int(now[0]), int(now[1]), int(now[2])))
left = left.split(',')[0]
print(left)
spisok = ['книга', 'свечи', 'цветы', 'лампа']


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
#РАБОТАЕТ С СУБМИТ
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
#РАБОТАЕТ С СУБМИТ
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
            return redirect(f'/main/{user.id}')
    return render_template('registration.html', title='Sign up', form=form)


@app.route('/')
def func():
    return render_template('base.html', title='Welcome')


@app.route('/main/<int:id>', methods=['GET', 'POST'])
@login_required
def main(id):
    db_sess = db_session.create_session()
    param = []
    for bd in db_sess.query(Birthday).filter(Birthday.user_id == id).all():
        param.append([bd.name, bd.date, bd.gifts])
    filter = Filter()
    return render_template('main.html', title='Home', param=param, filter=filter, add_link=f'/add/{id}',
                           birthday_link=f'/birthday/{id}')


@app.route('/add/<int:id>', methods=['GET', 'POST'])
@login_required
#РАБОТАЕТ С СУБМИТ
def add(id):
    form = BirthdayForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        bd = Birthday(name=form.name.data, date=form.date.data, gifts=form.presents.data, user_id=id)
        session.add(bd)
        session.commit()
        user = session.query(User).filter(User.id == id).first()
        bds = []
        for bd in session.query(Birthday).filter(Birthday.user_id == id).all():
            bds.append(str(bd.id))
        user.birthdays = ', '.join(bds)
        session.commit()
        return redirect(f'/main/{id}')
    return render_template('add_date.html', title='Adding birthday', form=form, id=id)


@app.route('/birthday/<int:id>', methods=['GET', 'POST'])
def birthday():
    return render_template('watch.html', name=name, date=date, left=left, spisok=spisok)


@app.route('/birthday/edit/<int:id>', methods=['GET', 'POST'])
def birthday_edit():
    return render_template('change.html', name=name, date=date, left=left, spisok=spisok)


if __name__ == '__main__':
    db_session.global_init("app/db/base.db")
    app.run(port=8081, host='127.0.0.1')