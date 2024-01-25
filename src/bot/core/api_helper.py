import requests
import json


class API:
    def __init__(self):
        self.api = 'http://api:5000'
        self.headers = {'Content-Type': 'application/json'}


    ##############################
    #        Healthchecks        #
    ##############################
    def healthcheck(self):
        """Returns the healthcheck status of the API"""
        return requests.get(f"{self.api}/hc").json()

    ##############################
    #           Settings         #
    ##############################
    def get_all_settings(self):
        """Returns all settings for all guilds in the Database"""
        return requests.get(f"{self.api}/settings/all").json()

    def get_settings_for_guild(self, guild_id):
        """Returns all settings for a guild in the Database"""
        return requests.get(f"{self.api}/settings/{guild_id}").json()

    # def update_settings(self, data):
    #     """Updates the settings for a guild in the Database"""
    #     response = requests.put(f"{self.api}/settings/", data=json.dumps(data), headers=self.headers)
    #     return response.json()

    ##############################
    #           Users            #
    ##############################
    def get_all_users(self):
        """Returns all users in the Database"""
        return requests.get(f"{self.api}/users/all").json()

    def get_specific_user(self, user_id):
        """Returns a user in the Database"""
        return requests.get(f"{self.api}/users/{user_id}").json()
