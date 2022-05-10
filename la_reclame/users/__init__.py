from flask import Blueprint

users = Blueprint('users', __name__, template_folder='templates', static_folder='static')

from la_reclame.users import routes