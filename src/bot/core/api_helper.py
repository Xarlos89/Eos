import os
import requests
import logging
import json

logger = logging.getLogger(__name__)

class API:
    def __init__(self):
        logger.info("Initializing API...")
        self.api = os.getenv('FLASK_URL')
        self.headers = {'Content-Type': 'application/json'}
        logger.info("API initialized.")


    ##############################
    #        Health checks       #
    ##############################

    def api_health_check(self):
        """Returns the healthcheck status of the API"""
        logger.debug("Bot called API healthcheck endpoint.")
        return requests.get(f"{self.api}/hc_api").json()

    def database_health_check(self):
        """Returns the healthcheck status of the API"""
        logger.debug("Bot called database healthcheck endpoint.")
        return requests.get(f"{self.api}/hc_db").json()


    ##############################
    #           Settings         #
    ##############################
    def get_one_setting(self, flag_id):
        """Retrieves one setting from the database"""
        logger.debug("Bot called get_one_setting endpoint.")
        return requests.get(f"{self.api}/settings/{flag_id}").json()

    def get_all_settings(self):
        """Retrieves all settings from the database"""
        logger.debug("Bot called the get_all_settings endpoint.")
        return requests.get(f"{self.api}/settings").json()

    def get_log_settings(self):
        """Retrieves all settings from the database"""
        logger.debug("Bot called the get_log_settings endpoint.")
        return requests.get(f"{self.api}/log_settings").json()

    def add_new_setting(self, name, value):
        """Adds a new setting to the database"""
        logger.debug(f"Bot called the add_new_setting endpoint. Setting to add: {name} - Setting value: {value}")
        data = {
            'name': name,
            'value': value
        }
        return requests.post(f"{self.api}/settings", json=data).json()

    def update_existing_setting(self, setting_id, new_value):
        """Updates an existing setting in the database"""
        logger.debug(f"Bot called the update_existing_setting endpoint. Setting ID: {setting_id} - New value: {new_value}")

        data = {
            'value': new_value
        }
        return requests.put(f"{self.api}/settings/{setting_id}", json=data).json()

    def delete_setting(self, setting_id):
        """Deletes a setting from the database"""
        logger.debug(f"Bot called the delete_setting endpoint. Setting ID: {setting_id}")
        return requests.delete(f"{self.api}/settings/{setting_id}").json()


    ##############################
    #            Points          #
    ##############################

    def add_user_to_points(self, user_id):
        logger.debug(f"Bot called the add_user_to_points endpoint. User ID: {user_id}")
        return requests.post(f"{self.api}/points/{user_id}/add").json()

    def delete_user_from_points(self, user_id):
        logger.debug(f"Bot called the delete_user_from_points endpoint. User ID: {user_id}")
        return requests.delete(f"{self.api}/points/{user_id}").json()

    def get_points(self, user_id):
        logger.debug(f"Bot called the get_points endpoint. User ID: {user_id}")
        return requests.get(f"{self.api}/points/{user_id}").json()

    def update_points(self, user_id, amount):
        logger.debug(f"Bot called the update_points endpoint. User ID: {user_id} - Points: {amount}")
        data = {'value': amount}
        return requests.post(f"{self.api}/points/{user_id}/update", json=data).json()

    def top_10(self):
        logger.debug("Bot called the top_10 endpoint.")
        return requests.get(f"{self.api}/points/top10").json()
