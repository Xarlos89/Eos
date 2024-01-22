from flask import Flask, jsonify


from api.routes.healthcheck import healthchecks
from api.routes.commands import command
from api.routes.errors import error


app = Flask(__name__)

# API routes
app.register_blueprint(healthchecks)
app.register_blueprint(command)

# Error Handlers
app.register_blueprint(error)

