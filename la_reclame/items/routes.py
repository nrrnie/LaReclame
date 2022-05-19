from flask import render_template, session, request, flash
from flask import redirect, url_for
from la_reclame.items import items
from la_reclame.models import Items, Users, Categories, PriceTypes, Reviews
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

    pictures = [item.main_picture] if item.main_picture else []
    pictures.extend(item.pictures.split(',') if item.pictures else [])
    item.pictures = pictures

    return render_template('item-page.html', user=session['user'], item=item, reviews=Reviews.query.filter_by(item_id=item_id))


@items.route('/add-item', methods=['GET', 'POST'])
@auth_required
def add_item():
    categories = Categories.query.order_by(Categories.id.asc()).all()
    if request.method == 'GET':
        return render_template('add-item.html', user=session['user'], categories=categories)

    main_picture = request.files.get('item-main-picture')
    main_picture = picturesDB.add_picture('item-pictures', main_picture) if main_picture.filename != '' else None

    image_paths = [picturesDB.add_picture('item-pictures', file)
                   for file in request.files.getlist('item-pictures') if file.filename != '']

    category_type = request.form.get('category-type')
    category_id = Categories.query.with_entities(Categories.id).filter_by(category_name=category_type).first()[0]

    title = request.form.get('item-title')
    description = request.form.get('item-description')

    price_type = PriceTypes[request.form.get('price-type').lower()]
    price = request.form.get('item-price', None)
    if price_type == PriceTypes.fixed and price is None:
        flash('At fixed price type you must fill price as well', 'danger')
        return render_template('add-item.html', user=session['user'], categories=categories)

    item = Items(user_id=session['user'].id, title=title, description=description,
                 pictures=','.join(image_paths), main_picture=main_picture, category_id=category_id,
                 price_type=price_type, price=price if price else 0)

    db.session.add(item)
    db.session.commit()

    flash('Item is added!', 'success')
    return redirect(url_for('items.add_item'))

@items.route('/<item_id>/add/review', methods=['GET', 'POST'])
@auth_required
def add_review(item_id: int):

    username = session['user'].username
    title = request.form.get('title')
    description = request.form.get('description')
    rating = request.form.get('rating')

    if None in [title, description, rating]:
        flash('Not all data was given for the review!', 'danger')

    if Items.query.get(item_id) is None:
        flash('Item with such ID was not found!', 'danger')

    review = Reviews(item_id=item_id, username=username, title=title, description=description, rating=rating)

    db.session.add(review)
    db.session.commit()

    flash('Review is added!', 'success')
    return redirect(url_for('items.item_page', item_id=item_id))