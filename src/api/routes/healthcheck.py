from flask import Blueprint, jsonify


# Define a Blueprint
healthchecks = Blueprint('healthchecks', __name__)


@healthchecks.route('/hc', methods=['GET'])
def healthcheck():
    """
    A simple healthcheck that returns an up status.
    """
    return jsonify({"status": "up"}), 200