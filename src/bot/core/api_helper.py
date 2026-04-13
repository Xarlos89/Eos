import logging
import os

import aiohttp
import requests

logger = logging.getLogger(__name__)

# Default timeout (seconds) for all API requests so a hung API can't block the bot.
REQUEST_TIMEOUT = 10


class API:
    def __init__(self):
        logger.info("Initializing API...")
        self.api = os.getenv("FLASK_URL")
        self.headers = {"Content-Type": "application/json"}
        logger.info("API initialized.")

    ##############################
    #        Health checks       #
    ##############################

    async def async_api_health_check(self):
        """Returns healthcheck status of the API"""
        logger.debug("Bot called API healthcheck endpoint.")
        timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{self.api}/hc_api") as response:
                return await response.json()

    async def async_database_health_check(self):
        """Returns the healcheck status of the DB"""
        logger.debug("Bot called database healthcheck endpoint.")
        timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{self.api}/hc_db") as response:
                return await response.json()

    ##############################
    #           Logging          #
    ##############################
    def get_one_log_setting(self, flag_id):
        """Retrieves one log setting from the database"""
        logger.debug("Bot called get_one_log_setting endpoint.")
        return requests.get(
            f"{self.api}/logging/{flag_id}", timeout=REQUEST_TIMEOUT
        ).json()

    def get_all_log_settings(self):
        """Retrieves all log settings from the database"""
        logger.debug("Bot called the get_all_log_settings endpoint.")
        return requests.get(f"{self.api}/logging", timeout=REQUEST_TIMEOUT).json()

    def add_new_log_setting(self, name, value):
        """Adds a new log setting to the database"""
        logger.debug(
            f"Bot called the add_new_log_setting endpoint. Log setting to add: {name} - Log setting value: {value}"
        )
        data = {"name": name, "value": value}
        return requests.post(
            f"{self.api}/logging", json=data, timeout=REQUEST_TIMEOUT
        ).json()

    def update_existing_log_setting(self, log_id, new_value):
        """Updates an existing log setting in the database"""
        logger.debug(
            f"Bot called the update_existing_log_setting endpoint. Log setting ID: {log_id} - New value: {new_value}"
        )

        data = {"value": new_value}
        return requests.put(
            f"{self.api}/logging/{log_id}", json=data, timeout=REQUEST_TIMEOUT
        ).json()

    def delete_log_setting(self, log_id):
        """Deletes a log setting from the database"""
        logger.debug(
            f"Bot called the delete_log_setting endpoint. Log setting ID: {log_id}"
        )
        return requests.delete(
            f"{self.api}/logging/{log_id}", timeout=REQUEST_TIMEOUT
        ).json()

    ##############################
    #           Settings         #
    ##############################
    def get_one_setting(self, flag_id):
        """Retrieves one setting from the database"""
        logger.debug("Bot called get_one_setting endpoint.")
        return requests.get(
            f"{self.api}/settings/{flag_id}", timeout=REQUEST_TIMEOUT
        ).json()

    def get_all_settings(self):
        """Retrieves all settings from the database"""
        logger.debug("Bot called the get_all_settings endpoint.")
        return requests.get(f"{self.api}/settings/0", timeout=REQUEST_TIMEOUT).json()

    def add_new_setting(self, name, value):
        """Adds a new setting to the database"""
        logger.debug(
            f"Bot called the add_new_setting endpoint. Setting to add: {name} - Setting value: {value}"
        )
        data = {"name": name, "value": value}
        return requests.post(
            f"{self.api}/settings", json=data, timeout=REQUEST_TIMEOUT
        ).json()

    def update_existing_setting(self, setting_id, new_value):
        """Updates an existing setting in the database"""
        logger.debug(
            f"Bot called the update_existing_setting endpoint. Setting ID: {setting_id} - New value: {new_value}"
        )

        data = {"value": new_value}
        return requests.put(
            f"{self.api}/settings/{setting_id}", json=data, timeout=REQUEST_TIMEOUT
        ).json()

    def delete_setting(self, setting_id):
        """Deletes a setting from the database"""
        logger.debug(
            f"Bot called the delete_setting endpoint. Setting ID: {setting_id}"
        )
        return requests.delete(
            f"{self.api}/settings/{setting_id}", timeout=REQUEST_TIMEOUT
        ).json()

    ##############################
    #            Roles           #
    ##############################
    def get_one_role(self, flag_id):
        """Retrieves one role from the database"""
        logger.debug("Bot called get_one_role endpoint.")
        return requests.get(
            f"{self.api}/role/{flag_id}", timeout=REQUEST_TIMEOUT
        ).json()

    def get_all_roles(self):
        """Retrieves all roles from the database"""
        logger.debug("Bot called the get_all_roles endpoint.")
        return requests.get(f"{self.api}/role", timeout=REQUEST_TIMEOUT).json()

    def add_new_role(self, name, value):
        """Adds a new role to the database"""
        logger.debug(
            f"Bot called the add_new_role endpoint. role to add: {name} - role value: {value}"
        )
        data = {"name": name, "value": value}
        return requests.post(
            f"{self.api}/role", json=data, timeout=REQUEST_TIMEOUT
        ).json()

    def update_existing_role(self, role_id, new_value):
        """Updates an existing role in the database"""
        logger.debug(
            f"Bot called the update_existing_role endpoint. role ID: {role_id} - New value: {new_value}"
        )

        data = {"value": new_value}
        return requests.put(
            f"{self.api}/role/{role_id}", json=data, timeout=REQUEST_TIMEOUT
        ).json()

    def delete_role(self, role_id):
        """Deletes a role from the database"""
        logger.debug(f"Bot called the delete_role endpoint. role ID: {role_id}")
        return requests.delete(
            f"{self.api}/role/{role_id}", timeout=REQUEST_TIMEOUT
        ).json()

    ##############################
    #            Points          #
    ##############################

    def add_user_to_points(self, user_id):
        logger.debug(f"Bot called the add_user_to_points endpoint. User ID: {user_id}")
        return requests.post(
            f"{self.api}/points/{user_id}/add", timeout=REQUEST_TIMEOUT
        ).json()

    def delete_user_from_points(self, user_id):
        logger.debug(
            f"Bot called the delete_user_from_points endpoint. User ID: {user_id}"
        )
        return requests.delete(
            f"{self.api}/points/{user_id}", timeout=REQUEST_TIMEOUT
        ).json()

    def get_points(self, user_id):
        logger.debug(f"Bot called the get_points endpoint. User ID: {user_id}")
        return requests.get(
            f"{self.api}/points/{user_id}", timeout=REQUEST_TIMEOUT
        ).json()

    def get_monthly_points(self, user_id):
        logger.debug(f"Bot called the get_monthly_points endpoint. User Id: {user_id}")
        return requests.get(f"{self.api}/points/monthly/{user_id}").json()

    def update_points(self, user_id, amount):
        logger.debug(
            f"Bot called the update_points endpoint. User ID: {user_id} - Points: {amount}"
        )
        data = {"value": amount}
        return requests.post(
            f"{self.api}/points/{user_id}/update", json=data, timeout=REQUEST_TIMEOUT
        ).json()

    def top_10(self):
        logger.debug("Bot called the top_10 endpoint.")
        return requests.get(
            f"{self.api}/points/top10", timeout=REQUEST_TIMEOUT
        ).json()

    def monthly_top_point_earner(self):
        logger.debug("Bot called monthly top point earner.")
        return requests.get(
            f"{self.api}/points/monthly/top", timeout=REQUEST_TIMEOUT
        ).json()

    def monthly_top_10(self):
        logger.debug("Bot called the monthly top_10 endpoint.")
        return requests.get(
            f"{self.api}/points/monthly/top10", timeout=REQUEST_TIMEOUT
        ).json()

    def reset_monthly_points(self):
        logger.debug("Bot called the reset monthly points endpoint.")
        return requests.delete(
            f"{self.api}/points/monthly/reset", timeout=REQUEST_TIMEOUT
        ).json()

    ##############################
    #        Parameters          #
    ##############################

    def get_parameter(self, parameter_name):
        logger.debug(f"Bot called parameters endpoint to get parameter {parameter_name}")
        return requests.get(
            f"{self.api}/parameters/{parameter_name}", timeout=REQUEST_TIMEOUT
        ).json()

    def set_parameter(self, parameter_name, parameter_value):
        logger.debug(f"Bot called parameters endpoint to set {parameter_name} to {parameter_value}")
        return requests.post(
            f"{self.api}/parameters/set/{parameter_name}/{parameter_value}", timeout=REQUEST_TIMEOUT
        ).json()
