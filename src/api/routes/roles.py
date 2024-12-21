from flask import Blueprint, jsonify, request
from flask import current_app as eos
import logging


logger = logging.getLogger(__name__)

# Define a Blueprint
role = Blueprint('roles', __name__)


@role.route('/role', methods=['GET'])
@role.route('/role/<int:role_id>', methods=['GET'])
def get_role(role_id=None):
    """
    Retrieve role from the database.

    :param role_id: Optional integer ID of a specific role
    :return: JSON response with role
    """
    if role_id is None:
        # Retrieve all role
        result = eos.db.get_roles()
    else:
        # Retrieve a single role
        result = eos.db.get_role(role_id)

    return jsonify(result, 200)

@role.route('/role/<role_id>', methods=['PUT'])
def update_role(role_id):
    """
    Update an existing role in the database.
    """
    if request.method == 'PUT':
        data = request.json
        result = eos.db.update_role(int(role_id), data['value'])
        return jsonify(result, 200)

    return jsonify({'message': 'improper request method'}, 405)

@role.route('/role', methods=['POST'])
def add_role():
    """
    Add a new role to the database.
    """
    if request.method == 'POST':
        data = request.json
        result = eos.db.add_role(data['name'], data['value'])
        return jsonify(result, 201)

    return jsonify({'message': 'improper request method'}, 405)

@role.route('/role/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    """
    Delete a specific role from the database.
    """
    if request.method == 'DELETE':
        result = eos.db.delete_role(role_id)
        return jsonify(result, 200)

    return jsonify({'message': 'improper request method'}, 405)
