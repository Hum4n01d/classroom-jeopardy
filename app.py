from os import environ, urandom

from base64 import b64encode
from json import dumps

from flask import Flask, render_template, g
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, emit
import pypugjs

from files import the_files
from accounts import accounts
from game import game

import models

app = Flask(__name__)
app.secret_key = urandom(24)

socketio = SocketIO(app)

@socketio.on('connection')
def connected():
    print('new connection')
    emit('new question', 'hi', broadcast=True)

@socketio.on('new question')
def new_question(question):
    print(question['answer'])
    print('question: '+str(question))
    emit('question', dumps(question), broadcast=True)

@socketio.on('question')
def question(q):
    print('got a question for the teacher:'+q)

@socketio.on('correct')
def correct(question):
    print('got correct: '+str(question))
    emit('correct', question, broadcast=True)

@socketio.on('incorrect')
def incorrect(question):
    print('got incorrect: '+str(question))
    emit('incorrect', question, broadcast=True)

app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

def encode(text):
    return str(b64encode(text.encode('ascii'))).strip("b").strip("'")

app.jinja_env.filters['encode'] = encode

app.register_blueprint(accounts)
app.register_blueprint(game)

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

if __name__ == '__main__':
    models.initialize()

    PORT = int(environ.get('PORT', 3000))
    HOST = '0.0.0.0'
    DEBUG = environ.get('DEBUG', False)

    socketio.run(app, port=PORT, host=HOST, debug=DEBUG, extra_files=the_files)
