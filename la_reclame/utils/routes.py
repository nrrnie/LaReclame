from flask import send_file
from la_reclame.utils import utils
from utils import picturesDB


@utils.route('/get-picture/<table>/<filename>', methods=['GET'])
def get_picture(table: str, filename: str):
    path = picturesDB.get_picture_path(table, filename)
    return send_file(path, mimetype='image/gif')

