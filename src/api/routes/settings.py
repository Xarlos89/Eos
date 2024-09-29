from flask import Blueprint, jsonify, request
from flask import current_app as eos
import logging


logger = logging.getLogger(__name__)

# Define a Blueprint
settings = Blueprint('settings', __name__)


@settings.route('/settings', methods=['GET'])
@settings.route('/settings/<int:setting_id>', methods=['GET'])
def get_settings(setting_id=None):
    """
    Retrieve settings from the database.

    :param setting_id: Optional integer ID of a specific setting
    :return: JSON response with settings
    """
    if setting_id is None:
        # Retrieve all settings
        result = eos.db.get_settings()
    else:
        # Retrieve a single setting
        result = eos.db.get_setting(setting_id)

    return jsonify(result, 200)


@settings.route('/settings/<setting_id>', methods=['PUT'])
def update_setting(setting_id):
    """
    Update an existing setting in the database.
    """
    if request.method == 'PUT':
        data = request.json
        result = eos.db.update_setting(int(setting_id), data['value'])
        return jsonify(result, 200)

    return jsonify({'message': 'improper request method'}, 405)

@settings.route('/settings', methods=['POST'])
def add_setting():
    """
    Add a new setting to the database.
    """
    if request.method == 'POST':
        data = request.json
        result = eos.db.add_setting(data['name'], data['value'])
        return jsonify(result, 201)

    return jsonify({'message': 'improper request method'}, 405)

@settings.route('/settings/<int:setting_id>', methods=['DELETE'])
def delete_setting(setting_id):
    """
    Delete a specific setting from the database.
    """
    if request.method == 'DELETE':
        result = eos.db.delete_setting(setting_id)
        return jsonify(result, 200)

    return jsonify({'message': 'improper request method'}, 405)
