from flask import Blueprint, jsonify, request
from flask import current_app as eos
import logging


logger = logging.getLogger(__name__)

# Define a Blueprint
parameters = Blueprint('parameters', __name__)


@parameters.route('/parameters/<parameter_name>', methods=['GET'])
def get_parameter(parameter_name):
    """
    Retrieve the value of a parameter from the DB.
    """
    try:
        result = eos.db.get_parameter(parameter_name)
        return jsonify(result), 200
    except Exception as err:
        logger.error(f"Error getting parameter {parameter_name}: {err}")
        return jsonify({"status": "error", "message": str(err)}), 400


@parameters.route('/parameters/set/<parameter_name>/<parameter_value>', methods=['POST'])
def set_parameter(parameter_name, parameter_value):
    """
    Set the value of a parameter in the DB
    """
    try:
        result = eos.db.set_parameter(parameter_name, parameter_value)
        return jsonify(result), 200
    except Exception as err:
        logger.error(f"Error setting parameter {parameter_name}: {err}")
        return jsonify({"status": "error", "message": str(err)}), 400
