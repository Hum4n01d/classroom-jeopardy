from json import loads
from flask import Blueprint, render_template, request, abort

import models

game = Blueprint('game', __name__, url_prefix='/game')

# @game.route('/create')
# def create():
#     from math_and_code_game import data
#
#     return render_template('game.pug', create=True, board=data)



@game.route('/<board_id>')
def play_game(board_id):
    try:
        board = models.Board.get(models.Board.id == board_id)
    except models.DoesNotExist:
        abort(404)

    board_data = loads(board.json_data)['game']

    return render_template('game.pug', board_data=board_data)

@game.route('/<board_id>/teacher')
def teacher_client(board_id):
    try:
        board = models.Board.get(models.Board.id == board_id)
    except models.DoesNotExist:
        abort(404)

    return render_template('teacher.pug')
