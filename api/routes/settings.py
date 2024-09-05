from flask import Blueprint, jsonify, request
from flask import current_app as eos


# Define a Blueprint
settings = Blueprint('settings', __name__)


@settings.route('/settings/all', methods=['GET'])
def get_all_settings():
    if request.method == 'GET':
        try:
            return jsonify(eos.db.read('settings'), 200)
        except Exception as e:
            return jsonify(f"Oops! Something went wrong: {e}", 404)

    else:
        return jsonify("Method not allowed", 405)


@settings.route('/settings/<guild_id>', methods=['GET'])
def get_settings_for_guild(guild_id):
    if request.method == 'GET':
        try:
            return jsonify(
                eos.db.read(
                    'settings', 'guild_id = %s', (guild_id,)
                ), 200)

        except Exception as e:
            return jsonify(f"Oops! Something went wrong: {e}", 404)
