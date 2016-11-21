from base64 import b64encode
from json import dumps
from os import environ, urandom

from flask import Flask, render_template, g
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, emit

import models
from accounts import accounts
from files import the_files
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

@socketio.on('no_answer')
def no_answer(question):
    emit('no_answer', question, broadcast=True)

@socketio.on('close_question')
def close_question():
    emit('close_question', broadcast=True)

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
    g.name = 'Jeopardy'
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

    try:
        models.User.create(
            username='Hum4n01d',
            password='pbkdf2:sha1:1000$yfvYZTxy$28a15bb8dbdb3a55f51b82b16edcb786355616ae',
            email='hum4n01d@icloud.com',
            is_admin=True
        )

    except models.IntegrityError:
        pass

    try:
        models.User.create(
            username='testq',
            password='pbkdf2:sha1:1000$ooCswSpt$a607935f180864677f761683f7bce4b1c4ca2c31',
            email='test@example.com'
        )

    except models.IntegrityError:
        pass

    PORT = int(environ.get('PORT', 3000))
    HOST = '0.0.0.0'
    DEBUG = environ.get('DEBUG', False)

    socketio.run(app, port=PORT, host=HOST, debug=DEBUG, extra_files=the_files)
