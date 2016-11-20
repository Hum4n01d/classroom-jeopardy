from json import loads

from flask import Blueprint, render_template, abort, g, request
from flask import redirect
from flask import url_for

import models

game = Blueprint('game', __name__, url_prefix='/game')


@game.route('/<board_id>')
# @login_required
def play(board_id):
    try:
        board = models.Board.get(models.Board.id == board_id)
    except models.DoesNotExist:
        abort(404)

    categories = list(board.category_set)
    board.category_set = categories

    for category in categories:
        category.question_set = list(category.question_set)

    return render_template('board.pug', board=board)


@game.route('/<board_id>/teacher')
# @login_required
def teacher(board_id):
    return render_template('teacher.pug')


@game.route('/create', methods=['GET', 'POST'])
# @login_required
def create():
    board = {
        'title': 'Board Title',
        'creator': {
            'username': g.user
        },
        'category_set': [
            {
                'title': 'Category Title',
                'question_set': [
                    {
                        'value': 200,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 400,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 600,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 800,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 1000,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                ]
            },
            {
                'title': 'Category Title',
                'question_set': [
                    {
                        'value': 200,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 400,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 600,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 800,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 1000,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                ]
            },
            {
                'title': 'Category Title',
                'question_set': [
                    {
                        'value': 200,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 400,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 600,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 800,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 1000,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                ]
            },
            {
                'title': 'Category Title',
                'question_set': [
                    {
                        'value': 200,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 400,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 600,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 800,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 1000,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                ]
            },
            {
                'title': 'Category Title',
                'question_set': [
                    {
                        'value': 200,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 400,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 600,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 800,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                    {
                        'value': 1000,
                        'question': 'Question text',
                        'answer': 'Question answer'
                    },
                ]
            }
        ]
    }

    if request.method == 'POST':
        json_data = loads(request.form['json_data'])
        board = models.create_my_game(json_data, g.user._get_current_object())

        return redirect(url_for('game.play', board_id=board.id))

    return render_template('create.pug', board=board)


@game.route('/all')
def all():
    try:
        boards = list(models.Board.select())
    except models.DoesNotExist:
        abort(404)

    return render_template('games_list.pug', boards=boards)
