import os
import logging
from flask import Flask, jsonify

from __logger__ import setup_logger
from routes.healthchecks import health_checks
from routes.settings import settings
from core.db_helper import DB

log = logging.getLogger(__name__)
setup_logger(
    level=int(os.getenv("LOG_LEVEL"))
    , stream_logs=bool(os.getenv("STREAM_LOGS")))


app = Flask(__name__)
app.db = DB()

# API routes
app.register_blueprint(health_checks)
app.register_blueprint(settings)