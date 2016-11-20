from flask import Blueprint, abort, render_template

import models

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/<username>')
def profile(username):
    try:
        profile_user = models.User.get(models.User.username == username)
    except models.DoesNotExist:
        abort(404)

    profile_user.board_set = list(profile_user.board_set)

    profile_user.parsed_joined_date = '{month}/{day}/{year}'.format(
        month=profile_user.joined_date.month,
        day=profile_user.joined_date.day,
        year=profile_user.joined_date.year
    )

    return render_template('profile.pug', profile_user=profile_user)
