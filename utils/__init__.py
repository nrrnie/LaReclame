from flask import session, redirect, url_for
import functools


def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('auth.login'))
        else:
            return func(*args, **kwargs)

    return wrapper
