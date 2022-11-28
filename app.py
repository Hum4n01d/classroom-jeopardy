from base64 import b64encode
from json import dumps
from os import environ, urandom

from flask import Flask, render_template, g
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, emit

import models
import config

from accounts import accounts
from game import game
from users import users

app = Flask(__name__)
app.secret_key = urandom(24)

socketio = SocketIO(app)


@socketio.on('new question')
def new_question(question):
    emit('question', dumps(question), broadcast=True)


@socketio.on('correct')
def correct(question):
    emit('correct', question, broadcast=True)


@socketio.on('incorrect')
def incorrect(question):
    emit('incorrect', question, broadcast=True)


@socketio.on('no answer')
def no_answer(question):
    emit('no answer', question, broadcast=True)


@socketio.on('close question')
def close_question():
    emit('close question', broadcast=True)

@socketio.on('start buzzing')
def start_buzzing(question):
    emit('start buzzing', question, broadcast=True)


app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')


def encode(text):
    return str(b64encode(text.encode('ascii'))).strip("b").strip("'")


app.jinja_env.filters['encode'] = encode

app.register_blueprint(accounts)
app.register_blueprint(game)
app.register_blueprint(users)


@app.context_processor
def inject_user():
    return dict(user=g.user._get_current_object())


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'accounts.log_in'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.db_proxy
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    '''Close the database connection after each request'''
    g.db.close()
    return response


@app.route('/')
def index():
    return render_template('index.pug')


@app.route('/presidents_game')
def presidents_game():
    return render_template('yay.pug')


if __name__ == '__main__':
    models.initialize()
    socketio.run(app, port=config.PORT, host=config.HOST, debug=config.DEBUG, extra_files=config.the_files)
