import requests
import json


class API:
    def __init__(self):
        self.api = 'http://api:5000'
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

    def update_settings(self, data, guild_id):
        """
        Updates the settings for a guild in the Database
        Expected in data:
            {
            "target": Name of setting to update
            , "channel_id": the ID of the channel to update
            , "status": True or False
            }
        """
        return requests.put(f"{self.api}/settings/{guild_id}", data=json.dumps(data), headers=self.headers)

    ##############################
    #           Users            #
    ##############################
    def get_all_users(self):
        """Returns all users in the Database"""
        return requests.get(f"{self.api}/users/all").json()

    def get_specific_user(self, user_id):
        """Returns a user in the Database"""
        return requests.get(f"{self.api}/users/{user_id}").json()
