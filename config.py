from dotenv import load_dotenv
from os import environ

from urllib.parse import quote_plus

load_dotenv()

db = {
    'user': environ.get('DATABASE_USER'),
    'password': environ.get('DATABASE_PASSWORD'),
    'host': environ.get('DATABASE_HOST'),
    'name': environ.get('DATABASE_NAME')
}


class Config:
    SECRET_KEY = 'asd'
    SESSION_TYPE = 'sqlalchemy'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db["user"]}:{quote_plus(db["password"])}@{db["host"]}/{db["name"]}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
