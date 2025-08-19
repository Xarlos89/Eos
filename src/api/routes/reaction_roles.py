from flask import Blueprint, jsonify, request
from flask import current_app as eos
import logging

logger = logging.getLogger(__name__)

# Define a Blueprint
reaction_roles = Blueprint('reaction_roles', __name__)


@role.route('/reaction_role', methods=['GET'])
@role.route('/reaction_role/<int:role_id>', methods=['GET'])
def get_reaction_role(role_id=None):
    """
    Retrieve role from the database.

    :param role_id: Optional integer ID of a specific role
    :return: JSON response with role
    """
    if role_id is None:
        # Retrieve all role
        result = eos.db.get_all_reaction_roles()
    else:
        # Retrieve a single role
        result = eos.db.get_reaction_role(role_id)

    return jsonify(result, 200)


@role.route('/reaction_role_category/<int:category_id>', methods=['GET'])
def get_reaction_role_category(category_id):
    """
    Retrieve role from the database.

    :param role_id: Optional integer ID of a specific category
    :return: JSON response with role
    """
    # Retrieve a single category
    result = eos.db.get_reaction_role_category(category_id)

    return jsonify(result, 200)


@role.route('/reaction_role/<role_id>', methods=['PUT'])
def update_reaction_role(role_id):
    """
    Update an existing role in the database.
    """
    if request.method == 'PUT':
        data = request.json
        result = eos.db.update_reaction_role(int(role_id), data['value'])
        return jsonify(result, 200)

    return jsonify({'message': 'improper request method'}, 405)


@role.route('/reaction_role', methods=['POST'])
def add_reaction_role():
    """
    Add a new role to the database.
    """
    if request.method == 'POST':
        data = request.json
        result = eos.db.add_reaction_role(data['name'], data['category'], data['value'])
        return jsonify(result, 201)

    return jsonify({'message': 'improper request method'}, 405)


@role.route('/reaction_role/<int:role_id>', methods=['DELETE'])
def delete_reaction_role(role_id):
    """
    Delete a specific role from the database.
    """
    if request.method == 'DELETE':
        result = eos.db.delete_reaction_role(role_id)
        return jsonify(result, 200)

    return jsonify({'message': 'improper request method'}, 405)
