from flask import Blueprint, jsonify


error = Blueprint('error', __name__)


@error.errorhandler(404)
def page_not_found():
    """ shit dont exist. """
    return jsonify(f"Page fell into the void.", 404)


@error.errorhandler(500)
def internal_error():
    """ It's dead mate. """
    return jsonify(f"API Error.", 500)