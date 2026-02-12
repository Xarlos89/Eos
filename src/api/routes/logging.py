from flask import Blueprint, jsonify, request
from flask import current_app as eos
import logging


logger = logging.getLogger(__name__)

# Define a Blueprint
logs = Blueprint('logging', __name__)

ALLOWED_LOG_NAMES = [
    'Verification Log',
    'Join Log',
    'Chat Log',
    'User Log',
    'Mod Log',
    'Server Log',
    'Error Log'
]

@logs.route('/logging', methods=['GET'])
def get_log_setting():
    """
    Retrieve logging settings from the database.
    Can take:
      - no params: returns all
      - integer param: returns one by id
      - string param: returns by name if in PREDEFINED_LOG_NAMES
    """
    log_id = request.args.get('id')
    log_name = request.args.get('name')

    if log_id is not None:
        try:
            result = eos.db.get_log_setting(int(log_id))
            return jsonify(result), 200
        except ValueError:
            return jsonify({"status": "error", "message": "id must be an integer"}), 400
    elif log_name is not None:
        if log_name in ALLOWED_LOG_NAMES:
            result = eos.db.get_log_setting_by_name(log_name) # TODO: Define me
            return jsonify(result), 200
        else:
            return jsonify({"status": "error", "message": "Invalid log name"}), 400

    else:
        result = eos.db.get_log_settings()
        return jsonify(result), 200

@logs.route('/logging/<log_identifier>', methods=['PUT'])
def update_log_setting(log_identifier):
    """
    Update an existing log setting by ID (int) or predefined name (string).
    """
    data = request.json
    value = data.get('value')
    if value is None:
        return jsonify({"status": "error", "message": "Missing required field: value"}), 400

    try:
        result = eos.db.update_logging(int(log_identifier), value)
        return jsonify(result), 200
    except ValueError:
        if log_identifier in ALLOWED_LOG_NAMES:
            result = eos.db.update_logging_by_name(log_identifier, value)
            return jsonify(result), 200
        else:
            return jsonify({"status": "error", "message": "Invalid log identifier"}), 400

@logs.route('/logging', methods=['POST'])
def add_log_setting():
    """
    Add a new setting to the database but only if the name is in the predefined allowed set.
    """
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        value = data.get('value')
        if not name or not value:
            return jsonify({"status": "error", "message": "Missing 'name' or 'value'"}), 400
        if name not in ALLOWED_LOG_NAMES:
            return jsonify({"status": "error", "message": f"Invalid log name: {name}"}), 400

        result = eos.db.add_log_setting(name, value)
        return jsonify(result), 201

    return jsonify({'message': 'improper request method'}), 405

@logs.route('/logging/<log_identifier>', methods=['DELETE'])
def delete_log_setting(log_identifier):
    """
    Delete a log setting by ID (int) or predefined name (string).
    """
    try:
        result = eos.db.delete_log_setting(int(log_identifier))
        return jsonify(result), 200
    except ValueError:
        if log_identifier in ALLOWED_LOG_NAMES:
            result = eos.db.delete_log_setting_by_name(log_identifier)
            return jsonify(result), 200
        else:
            return jsonify({"status": "error", "message": "Invalid log identifier"}), 400