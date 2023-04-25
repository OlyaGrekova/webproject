from flask import Flask, redirect, render_template
from flask_login import login_required, LoginManager, login_user
import datetime as dt

from app.data.birthdays import Birthday
from app.data.users import User
from forms import RegistrationForm, LoginForm, Filter, BirthdayForm, Main1, Main2, Main3, Watch, ChangeSave, ChangeDel

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
    global id
    form = RegistrationForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        if form.password.data == form.password_again.data:
            user = User(name=form.name.data, surname=form.surname.data, age=form.age.data, email=form.email.data)
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            login_user(user)
            id = user.id
            return redirect(f'/main/{user.id}')
    return render_template('registration.html', title='Sign up', form=form)


@app.route('/')
def func():
    return render_template('base.html', title='Welcome')


@app.route('/main/<int:id>')
@login_required
def main(id):
    db_sess = db_session.create_session()
    # param = db_sess.query(Birthday).all()
    param = [["Nastya", "02.03", "anime figure"], ["Julia", "13.07", "candle"], ["Olya", "16.09", "plane ticket"]]
    filter = Filter()
    form1 = Main1()
    form2 = Main2()
    form3 = Main3()
    if form1.validate_on_submit():
        return redirect("/main")
    if form2.validate_on_submit():
        return redirect("/main")
    if form3.validate_on_submit():
        return redirect("/main")
    return render_template('main.html', title='Home', param=param, filter=filter, form1=form1, form2=form2, form3=form3)


@app.route('/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add(id):
    form = BirthdayForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        print(load_user(id).birthdays)
        load_user(id).birthdays = ', '.join(load_user(id).birthdays.split().append(str(len(session.query(Birthday).all()) + 1)))
        session.commit()
        bd = Birthday(name=form.name.data, date=form.date.data, gifts=form.presents.data)
        session.add(bd)
        session.commit()
        return redirect('/main')
    return render_template('add_date.html', title='Adding birthday', form=form)


@app.route('/watch', methods=['GET', 'POST'])
def birthday():
    form = Watch()
    if form.validate_on_submit():
        return redirect("/main")
    return render_template('watch.html', form=form, name=name, date=date, left=left, spisok=spisok)


@app.route('/change', methods=['GET', 'POST'])
def birthday_edit():
    form1 = ChangeSave()
    form2 = ChangeDel()
    if form1.validate_on_submit():
        return redirect("/main")
    if form2.validate_on_submit():
        return redirect("/main")
    return render_template('change.html', form1=form1, form2=form2, name=name, date=date, left=left, spisok=spisok)


if __name__ == '__main__':
    db_session.global_init("app/db/base.db")
    app.run(port=8081, host='127.0.0.1')