from flask import Flask, jsonify

from api.utilities.db_helper import DB

from api.routes.healthcheck import healthchecks
from api.routes.settings import settings
from api.routes.users import users

app = Flask(__name__)
app.db = DB()

# API routes
app.register_blueprint(healthchecks)
app.register_blueprint(settings)
app.register_blueprint(users)



