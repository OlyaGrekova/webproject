from flask import Flask

from app.data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/main')
def main():
    return "test"


if __name__ == '__main__':
    db_session.global_init("db/base.db")
    app.run(port=8081, host='127.0.0.1')