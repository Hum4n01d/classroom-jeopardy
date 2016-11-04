from peewee import SqliteDatabase, PostgresqlDatabase
from os import environ
from urllib import parse

use_heroku_postgres = environ.get('DATABASE_URL', False)
# use_heroku_postgres = True

if use_heroku_postgres:
    database_url = environ['DATABASE_URL']

    parse.uses_netloc.append('postgres')
    url = parse.urlparse(database_url)
    db = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
else:
    db = SqliteDatabase('jeopardy.db')
