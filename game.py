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

    board_data = eval(board.json_data)

    return render_template('game.pug', board_data=board_data)
