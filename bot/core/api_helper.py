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
        """Returns all settings for all guilds in the Database"""
        return requests.get(f"{self.api}/settings/all").json()

    def get_settings_for_guild(self, guild_id):
        """Returns all settings for a guild in the Database"""
        return requests.get(f"{self.api}/settings/{guild_id}").json()
