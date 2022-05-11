from flask import Blueprint

api = Blueprint('api', __name__)

from la_reclame.api import routes
