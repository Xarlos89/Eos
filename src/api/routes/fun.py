from flask import Blueprint, jsonify, request
from flask import current_app as eos
from api.utilities import validators as v
from api.utilities import functions as f

# Define a Blueprint
test = Blueprint('fun', __name__)


@test.route('/read_db', methods=['GET'])
def read_db():
    """ Grabs all commands. """
    if request.method == 'GET':
        try:
            settings = eos.db.read('settings')
            return jsonify(settings, 200)
        except Exception as e:
            return jsonify(f"Oops! Something went wrong: {e}", 404)
