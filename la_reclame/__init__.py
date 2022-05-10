from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)

    return app