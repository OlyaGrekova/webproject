from flask import Flask, redirect, render_template
from flask_login import login_required, LoginManager, login_user
import datetime as dt
from requests import request

from app.data.birthdays import Birthday
from app.data.users import User
from forms import RegistrationForm, LoginForm, Filter, BirthdayForm, ChangeForm

from app.data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

filter_state = 'all'
key_state = 0
month = {"January": '01', "February": '02', "March": '03', "April": '04', "May": '05', "June": '06', "July": '07',
         "August": '08', "September": '09', "October": '10', "November": '11', "December": '12'}


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def apply_filters(filter_form, param):
    param2 = []
    if not filter_form.filter.data:
        choice = 'all'
    else:
        choice = filter_form.filter.data
    print(choice)
    if choice == 'all':
        param2 = param
    elif choice == 'next week':
        for i in param:
            date = '.'.join(i[1].split('.')[:-1]) + '.' + str((dt.datetime.now().date())).split('-')[0]
            now = str((dt.datetime.now().date())).split('-')
            left = str(dt.date(int(date.split('.')[2]), int(date.split('.')[1]), int(date.split('.')[0])) - dt.date(
                int(now[0]), int(now[1]), int(now[2]))).split(',')[0]
            if left <= 7:
                param2.append(i)
    elif choice == 'next month':
        for i in param:
            date = '.'.join(i[1].split('.')[:-1]) + '.' + str((dt.datetime.now().date())).split('-')[0]
            now = str((dt.datetime.now().date())).split('-')
            left = str(dt.date(int(date.split('.')[2]), int(date.split('.')[1]), int(date.split('.')[0])) - dt.date(
                int(now[0]), int(now[1]), int(now[2]))).split(',')[0]
            if left <= 30:
                param2.append(i)
    else:
        for i in param:
            m = i[1].split('.')[1]
            if m == month[choice]:
                param2.append(i)
    return param2


@app.route('/login', methods=['GET', 'POST'])
# РАБОТАЕТ С СУБМИТ
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(f"/main/{user.id}")
        return render_template('authorization.html', message="Wrong data", form=form)
    return render_template('authorization.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
# РАБОТАЕТ С СУБМИТ
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
    ids = []
    for bd in db_sess.query(Birthday).filter(Birthday.user_id == id).all():
        param.append([bd.name, bd.date, bd.gifts])
        ids.append(str(bd.id))
    filter_form = Filter()
    param = apply_filters(filter_form, param)
    return render_template('main.html', title='Home', param=param, add_link=f'/add/{id}',
                           birthday_link=f'/birthday/', ids=ids, length=len(param), id=str(id),
                           filter='all', filter_form=filter_form)


@app.route('/main/<int:id>/<int:bd_id>', methods=['GET', 'POST'])
@login_required
def main_delete(id, bd_id):
    db_sess = db_session.create_session()
    bd = db_sess.query(Birthday).filter(Birthday.id == bd_id).first()
    db_sess.delete(bd)
    db_sess.commit()
    return redirect(f'/main/{id}')


@app.route('/sort_bd/<int:id>/<int:key>', methods=['GET', 'POST'])
@login_required
def sort_bd(id, key):
    print('yup')
    global key_state
    key_state = key
    return redirect(f'/main/{id}')


@app.route('/filter_bd/<int:id>/<choice>', methods=['GET', 'POST'])
@login_required
def filter_bd(id, choice):
    filter_form = Filter()
    print(choice)
    global filter_state
    filter_state = choice
    return redirect(f'/main/{id}')


@app.route('/add/<int:id>', methods=['GET', 'POST'])
@login_required
# РАБОТАЕТ С СУБМИТ
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
def birthday(id):
    session = db_session.create_session()
    bd = session.query(Birthday).filter(Birthday.id == id).first()
    spisok = bd.gifts.split(', ')
    date = dt.date(dt.datetime.today().year, int(str(bd.date).split()[0].split('-')[1]),
                   int(str(bd.date).split()[0].split('-')[2]))
    now = dt.date.today()
    left = (date - now).days
    if left < 0:
        left = 360 + left
    user = session.query(User).filter(User.birthdays.like(f'%{id}%')).first()
    return render_template('watch.html', name=bd.name, date=bd.date, left=left, spisok=spisok,
                           link=f'/birthday/edit/{id}', link2=f'/main/{user.id}')


@app.route('/birthday/edit/<int:id>', methods=['GET', 'POST'])
def birthday_edit(id):
    session = db_session.create_session()
    bd = session.query(Birthday).filter(Birthday.id == id).first()
    spisok = bd.gifts.split(', ')
    date = dt.date(dt.datetime.today().year, int(str(bd.date).split()[0].split('-')[1]),
                   int(str(bd.date).split()[0].split('-')[2]))
    now = dt.date.today()
    left = (date - now).days
    if left < 0:
        left = 360 + left
    form = ChangeForm()
    if form.validate_on_submit():
        print('save')
        if form.name.data:
            bd.name = form.name.data
            session.commit()
        if form.date.data:
            bd.date = form.date.data
            session.commit()
        if form.presents.data:
            bd.gifts = form.presents.data
            session.commit()
        return redirect(f'/birthday/{id}')
    return render_template('change.html', form=form, name=bd.name, date=bd.date, left=left, spisok=spisok,
                           link=f'/birthday/{id}')


if __name__ == '__main__':
    db_session.global_init("app/db/base.db")
    app.run(port=8081, host='127.0.0.1')
