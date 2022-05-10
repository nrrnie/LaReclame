from flask import render_template
from la_reclame.items import items


@items.route('/')
def items_home():
    return render_template('items.html')
