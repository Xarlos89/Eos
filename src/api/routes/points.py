from flask import Blueprint, jsonify, request
from flask import current_app as eos

# Define a Blueprint
points = Blueprint('points', __name__)

@points.route('/points/<user_id>', methods=['GET'])
def get_points():
    """
    Retrieve points from the database.
    """
    try:
        result = eos.db.get_points_for_user(user_id)
        return jsonify(result), 200
    except Exception as err:
        eos.log.error(f"Error fetching points: {err}")
        return jsonify({"status": "error", "message": str(err)}), 500

@points.route('/points/<user_id>/update', methods=['POST'])
def update_points():
    """
    Update points for a user.
    """
    try:
        data = request.json
        if 'value' not in data:
            return jsonify({"status": "error", "message": "Missing required field: value"}), 400

        result = eos.db.update_points(user_id, data['value'])
        return jsonify(result), 200
    except ValueError as ve:
        eos.log.error(f"Invalid input: {ve}")
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as err:
        eos.log.error(f"Error updating points: {err}")
        return jsonify({"status": "error", "message": str(err)}), 500

@points.route('/points/<user_id>/add', methods=['POST'])
def add_user_to_points():
    """
    Add a new user to the points table.
    """
    try:
        result = eos.db.add_user_to_points(user_id)
        return jsonify(result), 201
    except ValueError as ve:
        eos.log.error(f"Invalid input: {ve}")
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as err:
        eos.log.error(f"Error adding user: {err}")
        return jsonify({"status": "error", "message": str(err)}), 500

@points.route('/points/<user_id>', methods=['DELETE'])
def remove_user_from_points():
    """
    Remove a user from the points table.
    """
    try:
        result = eos.db.remove_user_from_points(user_id)
        return jsonify(result), 200
    except ValueError as ve:
        eos.log.error(f"Invalid input: {ve}")
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as err:
        eos.log.error(f"Error removing user: {err}")
        return jsonify({"status": "error", "message": str(err)}), 500
