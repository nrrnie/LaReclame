from flask import render_template
from la_reclame.users import users
from la_reclame.models import Users
from utils import auth_required


@users.route('/<username>')
@auth_required
def profile(username: str):
    user = Users.query.filter_by(username=username).first()

    if user is None:
        return '404\nUser not found'

    return render_template('profile.html', user=user)
