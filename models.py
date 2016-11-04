from datetime import datetime
from peewee import *
from flask_login import UserMixin

from db_init import db

db_proxy = Proxy()
db_proxy.initialize(db)

class BaseModel(Model):
    class Meta:
        database = db_proxy

# Users
class User(UserMixin, BaseModel):
    username = CharField(max_length=15, unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_date = DateTimeField(default=datetime.now)

class Board(BaseModel):
    name = CharField()
    json_data = TextField()

def initialize():
    db_proxy.connect()
    db_proxy.create_tables([User, Board], safe=True)
    db_proxy.close()
