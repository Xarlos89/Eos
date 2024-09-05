
from flask import Blueprint, jsonify, request
from flask import current_app as doopbot


# Define a Blueprint
health_checks = Blueprint('health_checks', __name__)


@health_checks.route('/hc_api', methods=['GET'])
def api_health_check():
    """
    A simple healthcheck that returns an up status.
    """

    if request.method == 'GET':
        return jsonify({'status': 'ok'}, 200)

    return jsonify({'message': 'improper request method'}, 405)


@health_checks.route('/hc_db', methods=['GET'])
def database_health_check():
    """
    A simple healthcheck that returns an up status.
    """
    if request.method == 'GET':
        try:
            hc = doopbot.db.database_health_check()
            return jsonify(hc, 200)

        except TypeError as ded:
            return jsonify({"status": "unhealthy", "error": "DB unreachable"}, 404)

    return jsonify({'message': 'improper request method'}, 404)
