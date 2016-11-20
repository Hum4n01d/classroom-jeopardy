from json import loads

from flask import Blueprint, render_template, abort, g, request
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import login_required

import models

game = Blueprint('game', __name__, url_prefix='/game')


@game.route('/<board_id>')
@login_required
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

@game.route('/<board_id>/delete')
@login_required
def delete(board_id):
    try:
        board = models.Board.get(models.Board.id == board_id)
    except models.DoesNotExist:
        abort(404)

    if not (board.creator == g.user or g.user.is_admin):
        abort(401)

    board.delete_instance()

    models.Question.delete().where(models.Question.board == board)
    models.Category.delete().where(models.Category.board == board)

    flash('Board deleted')

    return redirect(url_for('index'))


@game.route('/<board_id>/teacher')
@login_required
def teacher(board_id):
    return render_template('teacher.pug')


@game.route('/create', methods=['GET', 'POST'])
@login_required
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
        board = models.create_my_game(g.user._get_current_object(), json_data)

        return redirect(url_for('game.play', board_id=board.id))

    return render_template('create.pug', board=board)

@game.route('/create/json', methods=['POST'])
@login_required
def create_json():
    json_data = loads(request.form['json_data'])
    board = models.create_my_game(g.user._get_current_object(), json_data)

    return redirect(url_for('game.play', board_id=board.id))

@game.route('/all')
def all():
    try:
        boards = list(models.Board.select())
    except models.DoesNotExist:
        abort(404)

    return render_template('games_list.pug', boards=boards)
