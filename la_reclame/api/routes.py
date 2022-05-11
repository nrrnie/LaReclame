from flask import request
from passlib.hash import sha256_crypt
from la_reclame.models import Users
from la_reclame.api import api
from la_reclame import db


@api.route('/auth/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if None in [username, password]:
        return dict(status='error', error='Not all data was given.')

    user = Users.query.filter_by(username=username).first()

    if user is None or not sha256_crypt.verify(password, user.password):
        return dict(status='error', error='Username or password is incorrect.')

    return dict(status='ok')


@api.route('/auth/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if None in [username, password, email]:
        return dict(status='error', error='Not all data was given.')

    if Users.query.filter_by(username=username).first() is not None:
        return dict(status='error', error='Username is already taken.')

    if Users.query.filter_by(email=email).first() is not None:
        return dict(status='error', error='Email is already taken.')

    user = Users(username=username, email=email, password=sha256_crypt.hash(password))
    db.session.add(user)
    db.session.commit()

    return dict(status='ok')
