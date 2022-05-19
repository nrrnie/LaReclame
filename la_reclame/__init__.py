from flask import Flask, redirect, url_for
from flask_session import Session, SqlAlchemySessionInterface
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy()
migrate = Migrate()
sess = Session()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from la_reclame import models

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)

        sess.init_app(app)
        SqlAlchemySessionInterface(app, db, 'sessions', 'sess_')
        db.create_all()

    from la_reclame.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    from la_reclame.users import users
    app.register_blueprint(users, url_prefix='/users')
    from la_reclame.items import items
    app.register_blueprint(items, url_prefix='/items')
    from la_reclame.utils import utils
    app.register_blueprint(utils, url_prefix='/utils')
    from la_reclame.api import api
    app.register_blueprint(api, url_prefix='/api')

    @app.route('/')
    def main():
        return redirect(url_for('items.items_home'))

    return app
