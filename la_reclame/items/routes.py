from flask import render_template
from la_reclame.items import items
from utils import auth_required


@items.route('/')
@auth_required
def items_home():
    return render_template('items.html')
