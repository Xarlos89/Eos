import unittest

from flask import Flask
from routes.healthchecks import health_checks
from routes.logging import logs
from routes.roles import role
from routes.settings import settings


class FakeDB:
    def __init__(self):
        self.db_unreachable = False

    def get_roles(self):
        return {"resource": "roles"}

    def update_role(self, role_id, value):
        return {"id": role_id, "value": value}

    def add_role(self, name, value):
        return {"name": name, "value": value}

    def delete_role(self, role_id):
        return {"deleted": role_id}

    def get_log_settings(self):
        return {"resource": "logging"}

    def update_logging(self, log_id, value):
        return {"id": log_id, "value": value}

    def add_log_setting(self, name, value):
        return {"name": name, "value": value}

    def delete_log_setting(self, log_id):
        return {"deleted": log_id}

    def get_settings(self):
        return {"resource": "settings"}

    def get_setting(self, setting_id):
        return {"id": setting_id}

    def update_setting(self, setting_id, value):
        return {"id": setting_id, "value": value}

    def add_setting(self, name, value):
        return {"name": name, "value": value}

    def delete_setting(self, setting_id):
        return {"deleted": setting_id}

    def database_health_check(self):
        if self.db_unreachable:
            raise TypeError("DB unreachable")

        return {"status": "healthy"}


def create_app():
    app = Flask(__name__)
    app.db = FakeDB()
    app.register_blueprint(health_checks)
    app.register_blueprint(logs)
    app.register_blueprint(settings)
    app.register_blueprint(role)
    return app


class RouteStatusCodeTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def assert_object_response(self, method, path, expected_status, json=None):
        response = getattr(self.client, method)(path, json=json)

        self.assertEqual(response.status_code, expected_status)
        self.assertIsInstance(response.get_json(), dict)

    def test_roles_routes_return_status_codes_outside_json_body(self):
        self.assert_object_response("get", "/role", 200)
        self.assert_object_response("put", "/role/1", 200, json={"value": "admin"})
        self.assert_object_response(
            "post",
            "/role",
            201,
            json={"name": "moderator", "value": "mod"},
        )
        self.assert_object_response("delete", "/role/1", 200)

    def test_logging_routes_return_status_codes_outside_json_body(self):
        self.assert_object_response("get", "/logging", 200)
        self.assert_object_response("put", "/logging/1", 200, json={"value": "on"})
        self.assert_object_response(
            "post",
            "/logging",
            201,
            json={"name": "joins", "value": "enabled"},
        )
        self.assert_object_response("delete", "/logging/1", 200)

    def test_settings_routes_return_status_codes_outside_json_body(self):
        self.assert_object_response("get", "/settings/0", 200)
        self.assert_object_response("put", "/settings/1", 200, json={"value": "on"})
        self.assert_object_response(
            "post",
            "/settings",
            201,
            json={"name": "prefix", "value": ">"},
        )
        self.assert_object_response("delete", "/settings/1", 200)

    def test_healthcheck_routes_return_status_codes_outside_json_body(self):
        self.assert_object_response("get", "/hc_api", 200)
        self.assert_object_response("get", "/hc_db", 200)

        self.app.db.db_unreachable = True
        self.assert_object_response("get", "/hc_db", 404)


if __name__ == "__main__":
    unittest.main()
