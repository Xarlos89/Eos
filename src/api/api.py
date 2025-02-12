import os
import logging
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from __logger__ import setup_logger

from routes.healthchecks import health_checks
from routes.logging import logs
from routes.settings import settings
from routes.points import points
from routes.roles import role
from routes.reaction_roles import reaction_roles

from core.db_helper import DB

logger = logging.getLogger(__name__)
setup_logger(
    level=int(os.getenv("API_LOG_LEVEL"))
    , stream_logs=bool(os.getenv("STREAM_LOGS")))

app = Flask(__name__)
app.db = DB()

# API routes
app.register_blueprint(health_checks)
app.register_blueprint(logs)
app.register_blueprint(settings)
app.register_blueprint(points)
app.register_blueprint(role)
app.register_blueprint(reaction_roles)


# Error handlers
@app.errorhandler(Exception)
def handle_exception(e):
    # Generic Application Errors
    app.logger.error(f"Unhandled exception: {str(e)}")

    # Return a JSON response with a generic error message
    return jsonify({
        "error": "An unexpected error occurred",
        "details": str(e)
    }), 500


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    # HTTP Exception Errors
    app.logger.error(f"HTTP exception: {str(e)}")

    # Return a JSON response with details about the HTTP error
    return jsonify({
        "error": str(e),
        "status_code": e.code,
        "description": e.description
    }), e.code
