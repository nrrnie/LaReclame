from flask import render_template, session
from la_reclame.users import users
from la_reclame.models import Users


@users.route('/<username>')
def profile(username: str):
    user = Users.query.filter_by(username=username).first()

    if user is None:
        return '404\nUser not found'

    return render_template('profile.html', user=user)
