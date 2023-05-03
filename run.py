import flask
from flask import Flask

import funcs
from app.data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

blueprint = flask.Blueprint(
    'birthdays',
    __name__,
    template_folder='templates'
)


if __name__ == '__main__':
    db_session.global_init("app/db/base.db")
    app.register_blueprint(funcs.blueprint)
    app.run(port=8081, host='127.0.0.1')