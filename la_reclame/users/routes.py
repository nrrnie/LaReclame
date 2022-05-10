from flask import render_template, request, session
from flask import flash
from la_reclame.users import users
from la_reclame.models import Users
from utils import auth_required
from la_reclame import db


@users.route('/<username>')
@auth_required
def profile(username: str):
    user = Users.query.filter_by(username=username).first()

    if user is None:
        return '404\nUser not found'

    return render_template('profile.html', user=user)


@users.route('/settings', methods=['GET', 'POST'])
@auth_required
def settings():
    if request.method == 'GET':
        return render_template('settings.html', user=session['user'])

    username = request.form.get('username')

    if Users.query.filter_by(username=username).first() is not None:
        flash('Username is already taken', 'danger')
    else:
        user = Users.query.get(session['user'].id)
        user.username = username
        db.session.commit()

        session['user'] = user

        flash('Info was updated', 'success')
    return render_template('settings.html', user=session['user'])
