from flask import Blueprint, jsonify
from ..utilities.db_helper import db

# Define a Blueprint
healthchecks = Blueprint('healthchecks', __name__)


@healthchecks.route('/hc-api', methods=['GET'])
def api_health_check():
    """
    A simple healthcheck that returns an up status.
    """
    return jsonify({'api': 'ok'}, 200)


@healthchecks.route('/hc-db', methods=['GET'])
def database_health_check():
    """
    A simple healthcheck that returns an up status.
    """
    hc = db.database_health_check()
    return jsonify(hc, 200)
