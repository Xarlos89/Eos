from flask import Blueprint, jsonify, request
from flask import current_app as eos
import logging


logger = logging.getLogger(__name__)

# Define a Blueprint
points = Blueprint('points', __name__)

@points.route('/points/<user_id>', methods=['GET'])
def get_points(user_id):
    """
    Retrieve points from the database.
    """
    try:
        result = eos.db.get_points_for_user(user_id)
        if result['status'] == 'ok':
            return jsonify(result), 200
        else:
            logger.warning(f'Error getting points for user: {result}')
            return jsonify(result), 400
    except Exception as err:
        logger.error(f"Error fetching points: {err}")
        return jsonify({"status": "error", "message": str(err)}), 400

@points.route('/points/<user_id>/update', methods=['POST'])
def update_points(user_id):
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
        logger.error(f"Invalid input: {ve}")
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as err:
        logger.error(f"Error updating points: {err}")
        return jsonify({"status": "error", "message": str(err)}), 400

@points.route('/points/<user_id>/add', methods=['POST'])
def add_user_to_points(user_id):
    """
    Add a new user to the points table.
    """
    try:
        result = eos.db.add_user_to_points(user_id)
        return jsonify(result), 201
    except ValueError as ve:
        logger.error(f"Invalid input: {ve}")
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as err:
        logger.error(f"Error adding user: {err}")
        return jsonify({"status": "error", "message": str(err)}), 400

@points.route('/points/<user_id>', methods=['DELETE'])
def remove_user_from_points(user_id):
    """
    Remove a user from the points table.
    """
    try:
        result = eos.db.remove_user_from_points(user_id)
        return jsonify(result), 200
    except ValueError as ve:
        logger.error(f"Invalid input: {ve}")
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as err:
        logger.error(f"Error removing user: {err}")
        return jsonify({"status": "error", "message": str(err)}), 400

@points.route('/points/top10', methods=['GET'])
def top10():
    """
    Grabs the top 10 point earners from the DB
    """
    try:
        result = eos.db.get_top_10()
        return jsonify(result), 200
    except Exception as err:
        logger.error(f"Error removing user: {err}")
        return jsonify({"status": "error", "message": str(err)}), 400
