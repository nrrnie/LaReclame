from werkzeug.datastructures import FileStorage
from base64 import decodebytes
from typing import Union
from uuid import uuid4
import os


class PicturesDB:
    def __init__(self):
        self.root_path = os.path.split(os.path.abspath(__name__))[0]

        self.database_path = os.path.join(self.root_path, 'pictures')
        if not os.path.exists(self.database_path):
            os.mkdir(self.database_path)
            print('Pictures Database created!')

        self.tables = ['profile-pictures', 'item-pictures']
        for table in self.tables:
            table_path = os.path.join(self.database_path, table)
            if not os.path.exists(table_path):
                os.mkdir(table_path)
                print('Table', table, 'created!')

    def add_picture(self, table: str, picture: FileStorage) -> Union[bool, str]:
        if table not in self.tables:
            print('Table', table, 'not in Tables list!')
            return False

        filename = self.get_random_image_name(picture.filename.split('.')[-1])

        table_path = os.path.join(self.database_path, table)
        picture.save(os.path.join(table_path, filename))

        return filename

    def get_picture_path(self, table: str, filename: str) -> str:
        if table not in self.tables:
            print('Table', table, 'not in Tables list!')
            return ''

        path = os.path.join(self.database_path, table)
        path = os.path.join(path, filename)
        return path

    def delete_picture(self, table: str, filename: str):
        if table not in self.tables:
            print('Table', table, 'not in Tables list!')
            return False

        path = os.path.join(self.database_path, table)
        path = os.path.join(path, filename)
        os.remove(path)

    def add_picture_from_app(self, table: str, encoded_image: str):
        if table not in self.tables:
            print('Table', table, 'not in Tables list!')
            return False

        filename = self.get_random_image_name('jpeg')

        path = os.path.join(self.database_path, table)
        path = os.path.join(path, filename)
        with open(path, "wb") as fh:
            fh.write(decodebytes(bytes(encoded_image, 'utf-8')))

        return filename

    @staticmethod
    def get_random_image_name(extension: str):
        return uuid4().__str__() + '.' + extension
