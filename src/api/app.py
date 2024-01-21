from flask import Flask, jsonify, request
from functions import *
from validators import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    A simple healthcheck that returns an up status.
    """
    return 'Suck my nutz', 200


@app.route('/hc', methods=['GET'])
def healthcheck():
    """
    A simple healthcheck that returns an up status.
    """
    return jsonify({"status": "up"}), 200


@app.route('/settings/commands/all', methods=['GET'])
def all_commands():
    """ Grabs all commands. """
    if request.method == 'GET':
        if db_exists():
            db = read_from_db_lol()
            if db:
                return jsonify(db, 200)
            return jsonify(f"No Data", 200)


@app.route('/settings/commands/<command>', methods=['GET', 'POST'])
def commands(command):
    """ Grabs the status of a command. """
    if request.method == 'GET':
        if command_exists(command):
            if read_from_db_lol()[command]:
                return jsonify(f"On", 200)
            return jsonify(f"Off", 200)
        return jsonify(f"{command} does not exist.", 400)

    """ Changes the status of a command. """
    if request.method == 'POST':
        if command_exists(command):
            if read_from_db_lol()[command]:
                write_to_db_lol(command, False)
                return jsonify(f"{command} : false", 200)
            if not read_from_db_lol()[command]:
                write_to_db_lol(command, True)
                return jsonify(f"{command} : true", 200)
        else:
            return jsonify(f"{command} not found.", 400)

    return jsonify(f"{request.method} not allowed", 400)


@app.route('/settings/commands/toggle-all/<status>', methods=['POST'])
def toggle_all(status):
    """ Grabs the status of a command. """
    if request.method == 'POST':
        if status == 'on':
            if read_from_db_lol():
                change_all_commands(status)
                return jsonify(f"On", 200)
            else:
                return jsonify(f"No DB connected.", 404)
        if status == 'off':
            if read_from_db_lol():
                change_all_commands(status)
                return jsonify(f"Off", 200)
        else:
            return jsonify(f"Status must be on/off", 404)
    else:
        return jsonify(f"{request.method} is not allowed", 404)


@app.errorhandler(404)
def page_not_found(error):
    """ shit dont exist. """
    return jsonify(f"Page fell into the void.", 404)


@app.errorhandler(500)
def internal_error(error):
    """ It's dead mate. """
    return jsonify(f"API Error.", 500)