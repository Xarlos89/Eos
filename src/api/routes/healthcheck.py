from flask import Blueprint, jsonify, request
from flask import current_app as eos

# Define a Blueprint
health_checks = Blueprint('health_checks', __name__)


@health_checks.route('/hc_api', methods=['GET'])
def api_health_check():
    """
    A simple healthcheck that returns an up status.
    """
    if request.method == 'GET':
        return jsonify({'status': 'ok'}, 200)

    return jsonify({'message': 'improper request method'}, 404)


@health_checks.route('/hc_db', methods=['GET'])
def database_health_check():
    """
    A simple healthcheck that returns an up status.
    """
    if request.method == 'GET':
        hc = eos.db.database_health_check()
        return jsonify(hc, 200)

    return jsonify({'message': 'improper request method'}, 404)

