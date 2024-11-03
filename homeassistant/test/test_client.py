import json
import os
from unittest import TestCase

from httmock import HTTMock, urlmatch

from homeassistant.client import command_service, get_entity_status

# Mock the environment variable
os.environ["HOMEASSISTANT_TOKEN"] = "fake_token"


@urlmatch(netloc=r"homeassistant\.local:8123")
def mock_api_responses(url, request):
    if url.path == "/api/states/light.living_room":
        return {
            "status_code": 200,
            "content": json.dumps(
                {"state": "on", "attributes": {"brightness": 255, "color_temp": 300}}
            ),
        }
    elif url.path == "/api/services/light/turn_on":
        return {"status_code": 200, "content": ""}

    return {"status_code": 404, "content": "Not Found"}


class TestHomeAssistantClient(TestCase):

    def test_get_entity_status(self):
        with HTTMock(mock_api_responses):
            result = get_entity_status("light.living_room")

        self.assertEqual(result["state"], "on")
        self.assertEqual(result["attributes"]["brightness"], 255)
        self.assertEqual(result["attributes"]["color_temp"], 300)

    def test_command_service(self):
        with HTTMock(mock_api_responses):
            response = command_service(
                "light",
                "turn_on",
                {"entity_id": "light.living_room", "brightness": 128},
            )

        # Since command_service doesn't return anything, we just check that it doesn't raise an exception
