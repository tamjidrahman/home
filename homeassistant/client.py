import os

from requests import post


class HAClient:
    def __init__(self):
        if not "HOMEASSISTANT_TOKEN" in os.environ:
            raise Exception("HOMEASSISTANT_TOKEN not set")
        token = os.environ["HOMEASSISTANT_TOKEN"]
        self._token = token
        self.url = "http://homeassistant.local:8123/api"

    def __call__(self, service: str, homeassistant_commandstr: str, data: dict):
        headers = {"Authorization": f"Bearer {self._token}"}
        url = f"{self.url}/services/{service}/{homeassistant_commandstr}"

        response = post(url, headers=headers, json=data)
        print(response.request.url)
        print(response.text)


client = HAClient()
