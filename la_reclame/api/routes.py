from flask import request
from passlib.hash import sha256_crypt
from la_reclame.models import Users
from la_reclame.api import api


@api.route('/auth/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if None in [username, password]:
        return dict(status='error', error='Not all data was given.')

    user = Users.query.filter_by(username=username)

    if user is None or not sha256_crypt.verify(password, user.password):
        return dict(status='error', error='Username or password is incorrect.')

    return dict(status='ok')
