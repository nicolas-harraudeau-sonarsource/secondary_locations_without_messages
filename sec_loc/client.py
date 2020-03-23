import requests
from requests.auth import HTTPBasicAuth

class Client:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def get(self, api, pages=100, page_size=500, **kwargs):
        params = {"p": 1, "ps": page_size, **kwargs}
        result = requests.get(f"{self.base_url}/{api}", auth=HTTPBasicAuth(self.token, ""), params=params)
        while result.status_code == requests.codes.ok and params["p"] < pages:
            yield result.json()
            params['p'] += 1
            result = requests.get(f"{self.base_url}/{api}", auth=HTTPBasicAuth(self.token, ""), params=params)
