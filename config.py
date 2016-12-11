from os import walk, path, environ

PORT = int(environ.get('PORT', 3000))
HOST = '0.0.0.0'
DEBUG = environ.get('DEBUG', False)

extra_dirs = ['templates/']
the_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                the_files.append(filename)
