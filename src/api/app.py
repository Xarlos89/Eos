from flask import Flask, jsonify

from api.utilities.db_helper import DB

from api.routes.healthcheck import healthchecks
from api.routes.commands import command
from api.routes.fun import test

app = Flask(__name__)
app.db = DB()

# API routes
app.register_blueprint(healthchecks)
app.register_blueprint(command)
app.register_blueprint(test)


