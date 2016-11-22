from datetime import datetime
from peewee import *
from flask_login import UserMixin

import json

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
    is_admin = BooleanField(default=False)

class BaseModel(Model):
    class Meta:
        database = db_proxy


class Board(BaseModel):
    title = CharField()
    date_created = DateTimeField(default=datetime.now)
    creator = ForeignKeyField(User)
    json_data = TextField()


class Category(BaseModel):
    title = CharField(max_length=1000)
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


def create_my_game(json_data, user):
    db_proxy.connect()

    raw_game = json_data['game']

    title = json_data['title']

    category_titles = [category['title'] for category in raw_game]

    categories_csv = ','.join(category_titles)

    board = Board.create(
        title=title,
        categories=categories_csv,
        creator=user,
        json_data=json_data
    )

    for category in raw_game:
        category_db = Category.create(
            title=category['title'],
            board=board
        )
        questions = category['questions']

        for question in questions:
            Question.create(
                value=question['value'],
                question=question['question'],
                answer=question['answer'],
                board=board,
                category=category_db
            )

    return board