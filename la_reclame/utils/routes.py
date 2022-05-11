from flask import request, send_file
from la_reclame.utils import utils
from utils import picturesDB


@utils.route('/get-picture', methods=['GET'])
def get_picture():
    table = request.values.get('table')
    filename = request.values.get('filename')

    path = picturesDB.get_picture_path(table, filename)
    return send_file(path, mimetype='image/gif')

