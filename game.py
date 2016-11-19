from json import loads
from flask import Blueprint, render_template, request, abort

import models

game = Blueprint('game', __name__, url_prefix='/game')

@game.route('/<board_id>')
def play_game(board_id):
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
def teacher_client(board_id):
    try:
        board = models.Board.get(models.Board.id == board_id)
    except models.DoesNotExist:
        abort(404)

    return render_template('teacher.pug')
