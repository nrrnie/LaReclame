from la_reclame import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    registered = db.Column(db.DATETIME, nullable=False, default=datetime.now)
    picture = db.Column(db.String(255))


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    created = db.Column(db.DATETIME, nullable=False, default=datetime.now)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    pictures = db.Column(db.Text)
    main_picture = db.Column(db.String(255))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created': str(self.created),
            'title': self.title,
            'description': self.description,
            'is_active': self.is_active,
            'pictures': self.pictures,
            'main_picture': self.main_picture,
        }
