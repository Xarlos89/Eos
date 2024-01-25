from flask import Blueprint, jsonify, request
from flask import current_app as eos


# Define a Blueprint
users = Blueprint('users', __name__)


@users.route('/users/all', methods=['GET'])
def get_users():
    if request.method == 'GET':
        try:
            return jsonify(eos.db.read('users'), 200)
        except Exception as e:
            return jsonify(f"Oops! Something went wrong: {e}", 404)

    else:
        return jsonify("Method not allowed", 405)


@users.route('/users/<user_id>', methods=['GET'])
def get_specific_user(user_id):
    if request.method == 'GET':
        try:
            return jsonify(eos.db.read('users', 'user_id = %s', (user_id,)), 200)
        except Exception as e:
            return jsonify(f"Oops! Something went wrong: {e}", 404)

    else:
        return jsonify("Method not allowed", 405)