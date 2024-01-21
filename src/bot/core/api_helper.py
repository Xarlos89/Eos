import requests


class API:
    def __init__(self):
        self.api = 'http://api:5000'

    def healthcheck(self):
        return requests.get(f"{self.api}/hc").text

    def all_commands(self):
        return requests.get(f"{self.api}/settings/commands/all").text
