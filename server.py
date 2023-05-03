import flask
from flask import Flask
from flask_login import LoginManager

import funcs
from app.data import db_session
from app.data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    db_session.global_init("app/db/base.db")
    app.register_blueprint(funcs.blueprint)
    app.run(port=8081, host='127.0.0.1')