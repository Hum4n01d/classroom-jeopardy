import json
import os
from datetime import datetime
from peewee import *

from db_init import db

db_proxy = Proxy()
db_proxy.initialize(db)

class BaseModel(Model):
    class Meta:
        database = db_proxy

class Board(BaseModel):
    title = CharField()
    date_created = DateTimeField(default=datetime.now)
    categories = TextField() #A csv

class Category(BaseModel):
    title = CharField()
    board = ForeignKeyField(Board)

class Question(BaseModel):
    value = IntegerField()
    question = TextField()
    answer = TextField()
    date_created = DateTimeField(default=datetime.now)
    board = ForeignKeyField(Board)
    category = ForeignKeyField(Category)

def initialize():
    db_proxy.connect()
    db_proxy.create_tables([Question, Category, Board], safe=True)
    db_proxy.close()

def create_my_game(raw_json):
    db_proxy.connect()

    raw_game = raw_json['game']

    title = raw_json['title']

    category_titles = [category['title'] for category in raw_game]

    categories_csv = ','.join(category_titles)

    board = Board.create(
        title=title,
        categories=categories_csv
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

# os.system('rm a.db')
initialize()

create_my_game(json.load(open('mathandcodegame.json')))