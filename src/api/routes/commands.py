from flask import Blueprint, jsonify, request
from api.utilities import validators as v
from api.utilities import functions as f

# Define a Blueprint
command = Blueprint('command', __name__)

@command.route('/settings/commands/all', methods=['GET'])
def all_commands():
    """ Grabs all commands. """
    if request.method == 'GET':
        try:
            if v.db_exists():
                db = f.read_from_db_lol()
                if db:
                    return jsonify(db, 200)
                return jsonify(f"No Data", 200)
            return jsonify(f"DB not connected.", 404)
        except Exception as e:
            return jsonify(f"Oops! Something went wrong: {e}", 404)

    return jsonify(f"{request.method} not allowed.")


@command.route('/settings/commands/<command>', methods=['GET', 'POST'])
def commands(command):
    """ Grabs the status of a command. """
    if request.method == 'GET':
        if v.command_exists(command):
            if f.read_from_db_lol()[command]:
                return jsonify(f"On", 200)
            return jsonify(f"Off", 200)
        return jsonify(f"{command} does not exist.", 400)

    """ Changes the status of a command. """
    if request.method == 'POST':
        if v.command_exists(command):
            if f.read_from_db_lol()[command]:
                f.write_to_db_lol(command, False)
                return jsonify(f"{command} : false", 200)
            if not f.read_from_db_lol()[command]:
                f.write_to_db_lol(command, True)
                return jsonify(f"{command} : true", 200)
        else:
            return jsonify(f"{command} not found.", 400)

    return jsonify(f"{request.method} not allowed", 400)


@command.route('/settings/commands/toggle-all/<status>', methods=['POST'])
def toggle_all(status):
    """ Grabs the status of a command. """
    if request.method == 'POST':
        if status == 'on':
            if f.read_from_db_lol():
                f.change_all_commands(status)
                return jsonify(f"On", 200)
            else:
                return jsonify(f"No DB connected.", 404)
        if status == 'off':
            if f.read_from_db_lol():
                f.change_all_commands(status)
                return jsonify(f"Off", 200)
        else:
            return jsonify(f"Status must be on/off", 404)
    else:
        return jsonify(f"{request.method} is not allowed", 404)
