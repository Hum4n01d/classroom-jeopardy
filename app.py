from flask import Flask, render_template
from os import environ, walk, path, urandom
from forms import ClueForm
from game import data
from hashlib import md5

import pyjade

app = Flask(__name__)

app.secret_key = urandom(24)

app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJsExtension')

@pyjade.register_filter('md5')
def hash_md5(text):
    return md5(text.encode('utf-8')).hexdigest()

app.jinja_env.filters['md5'] = hash_md5

@app.route('/')
def index():
    return render_template('index.jade', data=data)

@app.route('/new_board', methods=['GET', 'POST'])
def new_board():
    form = ClueForm()

    if form.validate_on_submit():
        pass

    return render_template('new_board.jade', form=form)

if __name__ == '__main__':
    production = not environ.get('DEBUG', False)

    if production:
        app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)))

    else:
        extra_dirs = ['templates/']
        extra_files = extra_dirs[:]
        for extra_dir in extra_dirs:
            for dirname, dirs, files in walk(extra_dir):
                for filename in files:
                    filename = path.join(dirname, filename)
                    if path.isfile(filename):
                        extra_files.append(filename)

        port = int(environ.get('PORT', 5000))
        debug = environ.get('DEBUG', False)

        app.run(debug=debug, port=port, host='0.0.0.0', extra_files=extra_files)
