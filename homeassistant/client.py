import os

from requests import get, post

TOKEN = os.getenv("HOMEASSISTANT_TOKEN")

URL = "http://homeassistant.local:8123/api"


def get_entity_status(entity_id: str):

    headers = {"Authorization": f"Bearer {TOKEN}"}
    url = f"{URL}/states/{entity_id}"

    response = get(url, headers=headers)
    # print(response.request.url)
    # print(response.text)

    return response.json()


def command_service(service: str, homeassistant_commandstr: str, data: dict):

    headers = {"Authorization": f"Bearer {TOKEN}"}
    url = f"{URL}/services/{service}/{homeassistant_commandstr}"

    response = post(url, headers=headers, json=data)
    # print(response.request.url)
    # print(response.text)
