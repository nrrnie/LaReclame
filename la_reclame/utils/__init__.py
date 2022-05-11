from flask import Blueprint

utils = Blueprint('utils', __name__, template_folder='templates', static_folder='static')

from la_reclame.utils import routes
