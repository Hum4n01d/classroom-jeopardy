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

class BaseModel(Model):
    class Meta:
        database = db_proxy

class Board(BaseModel):
    title = CharField()
    date_created = DateTimeField(default=datetime.now)
    categories = TextField()  # A csv

class Category(BaseModel):
    title = CharField()
    board = ForeignKeyField(Board)

    def __str__(self):
        return self.title

class Question(BaseModel):
    value = IntegerField()
    question = TextField()
    answer = TextField()
    date_created = DateTimeField(default=datetime.now)
    board = ForeignKeyField(Board)
    category = ForeignKeyField(Category)

def initialize():
    db_proxy.connect()
    db_proxy.create_tables([User, Question, Category, Board], safe=True)
    db_proxy.close()
