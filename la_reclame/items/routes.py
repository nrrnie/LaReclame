from flask import render_template, session, request, flash
from la_reclame.items import items
from la_reclame.models import Items, Users
from la_reclame import db
from utils import auth_required


@items.route('/')
@auth_required
def items_home():
    return render_template('items.html', user=session['user'], items=Items.query.all())


@items.route('/add-item', methods=['GET', 'POST'])
@auth_required
def add_item():
    if request.method == 'GET':
        return render_template('add-item.html', user=session['user'])

    title = request.form.get('item-title')
    description = request.form.get('item-description')

    item = Items(user_id=session['user'].id, title=title, description=description)
    db.session.add(item)
    db.session.commit()

    flash('Item is added!', 'success')
    return render_template('add-item.html', user=session['user'])



