import os
import requests
import json


class API:
    def __init__(self):
        self.api = os.getenv('FLASK_URL')
        self.headers = {'Content-Type': 'application/json'}

    ##############################
    #        Health checks       #
    ##############################

    def api_health_check(self):
        """Returns the healthcheck status of the API"""
        return requests.get(f"{self.api}/hc_api").json()

    def database_health_check(self):
        """Returns the healthcheck status of the API"""
        return requests.get(f"{self.api}/hc_db").json()


    ##############################
    #           Settings         #
    ##############################
    def get_all_settings(self):
        """Retrieves all settings from the database"""
        return requests.get(f"{self.api}/settings").json()

    def add_new_setting(self, name, value):
        """Adds a new setting to the database"""
        data = {
            'name': name,
            'value': value
        }
        return requests.post(f"{self.api}/settings", json=data).json()

    def update_existing_setting(self, setting_id, new_value):
        """Updates an existing setting in the database"""
        data = {
            'value': new_value
        }
        return requests.put(f"{self.api}/settings/{setting_id}", json=data).json()

    def delete_setting(self, setting_id):
        """Deletes a setting from the database"""
        return requests.delete(f"{self.api}/settings/{setting_id}").json()