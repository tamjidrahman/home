import os
from typing import Any

from requests import get, post

TOKEN = os.getenv("HOMEASSISTANT_TOKEN")

URL = "http://homeassistant.local:8123/api"


def get_entity_status(entity_id: str) -> dict[str, Any]:

    headers = {"Authorization": f"Bearer {TOKEN}"}
    url = f"{URL}/states/{entity_id}"

    response = get(url, headers=headers)

    resp = response.json()

    return resp


def command_service(
    service: str, homeassistant_commandstr: str, data: dict
) -> dict[str, Any]:

    headers = {"Authorization": f"Bearer {TOKEN}"}
    url = f"{URL}/services/{service}/{homeassistant_commandstr}"

    response = post(url, headers=headers, json=data)

    resp = response.json()

    return resp
