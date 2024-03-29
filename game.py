from json import loads, dumps

from flask import Blueprint, render_template, abort, g, request, jsonify
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import login_required

import models
import config

game = Blueprint('game', __name__, url_prefix='/game')


@game.route('/<board_id>')
def play(board_id):
    try:
        board = models.Board.get(models.Board.id == board_id)
    except models.DoesNotExist:
        abort(404)

    categories = list(board.category_set)
    board.category_set = categories

    for category in categories:
        questions = category.question_set.order_by(models.Question.value)

        category.question_set = list(questions)

    return render_template('board.pug', board=board)

@game.route('/<board_id>/json')
@login_required
def get_json(board_id):
    try:
        board = models.Board.get(models.Board.id == board_id)
    except models.DoesNotExist:
        abort(404)

    json_data = loads(board.json_data)

    return jsonify(json_data)


@game.route('/<board_id>/teacher')
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
        try:
            json_data = loads(request.form['json_data'])

            board = models.create_my_game(
                user=g.user._get_current_object(),
                json_data=json_data
            )
        except:
            abort(400)

        return redirect(url_for('game.play', board_id=board.id))

    return render_template('create.pug', board=board)


@game.route('/<board_id>/delete')
@login_required
def delete(board_id):
    try:
        board = models.Board.get(models.Board.id == board_id)
    except models.DoesNotExist:
        abort(404)

    if not (board.creator == g.user or g.user.is_admin):
        abort(401)

    models.Question.delete().where(models.Question.board == board)
    models.Category.delete().where(models.Category.board == board)

    board.delete_instance()

    flash('Board deleted')

    return redirect(url_for('index'))


@game.route('/create/json')
@login_required
def create_json():
    return render_template('create_json.pug')


@game.route('/all')
def all():
    try:
        boards = list(models.Board.select())
    except models.DoesNotExist:
        abort(404)

    return render_template('games_list.pug', boards=boards)


if config.DEBUG:
    login_required(play)
    login_required(teacher)