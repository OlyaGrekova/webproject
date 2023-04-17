from flask import Flask
from flask_login import login_required

from app.data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    return "test"


@app.route('/main')
@login_required
def main():
    pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    pass


@app.route('/birthday/<int:id>', methods=['GET', 'POST'])
@login_required
def birthday(id):
    pass


@app.route('/birthday/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def birthday_edit(id):
    pass


if __name__ == '__main__':
    db_session.global_init("db/base.db")
    app.run(port=8081, host='127.0.0.1')