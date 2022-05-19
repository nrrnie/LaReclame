from itsdangerous import URLSafeTimedSerializer
from flask import request, url_for, send_file
from passlib.hash import sha256_crypt
from la_reclame.models import Users, Items, Categories
from la_reclame.api import api
from la_reclame import db
from utils import picturesDB, send_email, PriceTypes
from urllib.parse import quote
from os import getenv

url_serializer = URLSafeTimedSerializer(getenv('SECRET_KEY'))


@api.route('/auth/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if None in [username, password]:
        return dict(status='error', error='Not all data was given.')

    user = Users.query.filter_by(username=username).first()

    if user is None or not sha256_crypt.verify(password, user.password):
        return dict(status='error', error='Username or password is incorrect.')

    if user.is_active is False:
        return dict(status='error', error='User was not activated yet.')

    return dict(status='ok', user=user.serialize())


@api.route('/auth/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if None in [username, password, email]:
        return dict(status='error', error='Not all data was given.')

    if Users.query.filter_by(username=username).first() is not None:
        return dict(status='error', error='Username is already taken.')

    if Users.query.filter_by(email=email).first() is not None:
        return dict(status='error', error='Email is already taken.')

    user = Users(username=username, email=email, password=sha256_crypt.hash(password))
    db.session.add(user)
    db.session.commit()

    token = url_serializer.dumps(email, salt=getenv('SECRET_KEY_EMAIL_CONFIRM'))
    token_link = url_for('auth.confirm_email', token=token, _external=True)

    send_email(email, token_link)

    return dict(status='ok')


@api.route('/items', methods=['POST'])
def get_items():
    search = request.form.get('search', '')
    if search != '':
        title_like = Items.title.like("%{}%".format(search))
        description_like = Items.description.like("%{}%".format(search))
        items_list = Items.query.filter(title_like | description_like)
    else:
        items_list = Items.query

    filter_by = request.form.get('filter_by', '')
    if filter_by != '':
        items_list = items_list.filter_by(category_id=filter_by).all()
    else:
        items_list = items_list.all()

    return dict(status='ok', items=items_list)


@api.route('/add/item', methods=['POST'])
def add_item():
    user_id = int(request.form.get('user_id'))
    category_id = int(request.form.get('category_id'))
    title = request.form.get('title')
    description = request.form.get('description')
    price_type = request.form.get('price_type')
    price = request.form.get('price')

    if None in [user_id, title, description, category_id, price_type] or price_type == 'fixed' and price is None:
        return dict(status='error', error='Not all data was given.')

    price = int(price) if price is not None else None

    if Users.query.get(user_id) is None:
        return dict(status='error', error='User with such id not found.')

    if Categories.query.get(category_id) is None:
        return dict(status='error', error='Category with such id not found.')

    item = Items(user_id=user_id, title=title, description=description, category_id=category_id,
                 price_type=PriceTypes[price_type], price=price)
    db.session.add(item)
    db.session.commit()

    return dict(status='ok')


@api.route('/update/profile-picture', methods=['POST'])
def update_profile_picture():
    user_id = request.form.get('user_id')
    encoded_image = request.form.get('encodedImage')

    if None in [user_id, encoded_image]:
        return dict(status='error', error='Not all data was given.')

    user = Users.query.get(user_id)

    if user is None:
        return dict(status='error', error='User with such ID does not exist.')

    filename = picturesDB.add_picture_from_app('profile-pictures', encoded_image)
    user.picture = filename
    db.session.commit()

    return dict(status='ok')


@api.route('/get-image', methods=['POST'])
def get_item_image():
    table = request.form.get('table')
    filename = request.form.get('filename')
    path = picturesDB.get_picture_path(table, filename)
    # return dict(status='ok', image=quote(open(path, 'rb').read(), safe=""))
    return dict(status='ok', image=open(path, 'rb').read())


@api.route('/categories', methods=['POST'])
def get_categories():
    categories = [category.serialize() for category in Categories.query.order_by(Categories.id.asc()).all()]

    return dict(status='ok', categories=categories)
