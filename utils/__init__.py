from flask import session, redirect, url_for
import functools
from utils.PicturesDB import PicturesDB
picturesDB = PicturesDB()


def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)

    return wrapper


def not_auth(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') is None:
            return func(*args, **kwargs)
        return redirect(url_for('items.items_home'))

    return wrapper
