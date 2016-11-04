#!/users/kent/virtualenvs/chap/bin/python3

from os import environ, urandom
from flask import Flask, render_template, g
from flask_login import LoginManager, current_user

from files import the_files
from accounts import accounts
from game import game

import models

app = Flask(__name__)

app.secret_key = urandom(24)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

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

@app.route('/favicon.ico')
def favicorn():
    return 'nope lol'

if __name__ == '__main__':
    models.initialize()

    app.debug = environ.get('DEBUG', False)
    app.port = environ.get('PORT', 3000)
    app.run(extra_files=the_files)
