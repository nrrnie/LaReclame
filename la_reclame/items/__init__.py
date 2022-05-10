from flask import Blueprint

items = Blueprint('items', __name__, template_folder='templates', static_folder='static')

from la_reclame.items import routes
