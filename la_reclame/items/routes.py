from flask import render_template, session, request, flash
from la_reclame.items import items
from la_reclame.models import Items, Users, Categories, PriceTypes
from la_reclame import db
from utils import auth_required, picturesDB


@items.route('/')
@auth_required
def items_home():
    return render_template('items.html', user=session['user'], items=Items.query.all())


@items.route('/<item_id>')
@auth_required
def item_page(item_id: int):
    item = Items.query.get(item_id)
    if item is None:
        return '404\nItem not found'

    return render_template('item-page.html', user=session['user'], item=item)


@items.route('/add-item', methods=['GET', 'POST'])
@auth_required
def add_item():
    if request.method == 'GET':
        return render_template('add-item.html', user=session['user'],
                               categories=Categories.query.order_by(Categories.id.asc()).all())

    main_picture = request.files.get('item-main-picture')
    main_picture = picturesDB.add_picture('item-pictures', main_picture) if main_picture != '' else None

    image_paths = [picturesDB.add_picture('item-pictures', file)
                   for file in request.files.getlist('item-pictures') if file.filename != '']

    category_type = request.form.get('category-type')
    title = request.form.get('item-title')
    description = request.form.get('item-description')
    price_type = PriceTypes[request.form.get('price-type').lower()]
    price = request.form.get('price', None)

    if price_type == PriceTypes.fixed and price is None:
        flash('At fixed price type you must fill price as well', 'danger')
        return render_template('add-item.html', user=session['user'],
                               categories=Categories.query.order_by(Categories.id.asc()).all())

    item = Items(user_id=session['user'].id, title=title, description=description,
                 pictures=','.join(image_paths), main_picture=main_picture)

    db.session.add(item)
    db.session.commit()

    flash('Item is added!', 'success')
    return render_template('add-item.html', user=session['user'])
