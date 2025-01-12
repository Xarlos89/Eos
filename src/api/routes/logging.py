from flask import Blueprint, jsonify, request
from flask import current_app as eos
import logging


logger = logging.getLogger(__name__)

# Define a Blueprint
logs = Blueprint('logging', __name__)


@logs.route('/logging', methods=['GET'])
@logs.route('/logging/<int:log_id>', methods=['GET'])
def get_log_setting(log_id=None):
    """
    Retrieve logging settings from the database.

    :param log_id: Optional integer ID of a specific setting
    :return: JSON response with log setting
    """
    if log_id is None:
        # Retrieve all log settings
        result = eos.db.get_log_settings()
    else:
        # Retrieve a single setting
        result = eos.db.get_log_setting(log_id)

    return jsonify(result, 200)

# @settings.route('/log_settings', methods=['GET'])
# def get_log_settings():
#     """
#     Retrieve log settings from the database.
#
#     :return: JSON response with settings
#     """
#     result = eos.db.get_log_settings()
#
#     return jsonify(result, 200)

@logs.route('/logging/<log_id>', methods=['PUT'])
def update_log_setting(log_id):
    """
    Update an existing setting in the database.
    """
    if request.method == 'PUT':
        data = request.json
        result = eos.db.update_logging(int(log_id), data['value'])
        return jsonify(result, 200)

    return jsonify({'message': 'improper request method'}, 405)

@logs.route('/logging', methods=['POST'])
def add_log_setting():
    """
    Add a new setting to the database.
    """
    if request.method == 'POST':
        data = request.json
        result = eos.db.add_log_setting(data['name'], data['value'])
        return jsonify(result, 201)

    return jsonify({'message': 'improper request method'}, 405)

@logs.route('/logging/<int:log_id>', methods=['DELETE'])
def delete_log_setting(log_id):
    """
    Delete a specific setting from the database.
    """
    if request.method == 'DELETE':
        result = eos.db.delete_log_setting(log_id)
        return jsonify(result, 200)

    return jsonify({'message': 'improper request method'}, 405)
