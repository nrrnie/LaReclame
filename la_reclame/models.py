from la_reclame import db
from datetime import datetime
from utils import PriceTypes


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    registered = db.Column(db.DATETIME, nullable=False, default=datetime.now)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    picture = db.Column(db.String(255))

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'registered': str(self.registered),
            'picture': self.picture,
        }


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    category_id = db.Column(db.Integer, index=True)
    created = db.Column(db.DATETIME, nullable=False, default=datetime.now)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    price_type = db.Column(db.Enum(PriceTypes), nullable=False)
    price = db.Column(db.Integer, index=True)
    pictures = db.Column(db.Text)
    main_picture = db.Column(db.String(255))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'created': str(self.created),
            'title': self.title,
            'description': self.description,
            'is_active': self.is_active,
            'price_type': self.price_type,
            'price': self.price,
            'pictures': self.pictures,
            'main_picture': self.main_picture,
        }


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False, unique=True)

    def serialize(self):
        return {
            'id': self.id,
            'category_name': self.category_name
        }
