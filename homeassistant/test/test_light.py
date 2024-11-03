from unittest.mock import patch

import pytest

from homeassistant.light import Light, LightCommand


@pytest.fixture
def mock_client():
    with patch("homeassistant.light.client") as mock:
        yield mock


def test_light_entity_id():
    assert Light.LivingRoom.entity_id == "light.living_room"
    assert Light.Kitchen.entity_id == "light.kitchen"
    assert Light.Bedroom.entity_id == "light.bedroom"


def test_light_autolight_entity_id():
    assert (
        Light.LivingRoom.autolight_entity_id
        == "automation.living_room_lights_on_occupancy"
    )
    assert (
        Light.Kitchen.autolight_entity_id
        == "automation.kitchen_dining_automated_lights"
    )
    assert (
        Light.DiningRoom.autolight_entity_id
        == "automation.kitchen_dining_automated_lights"
    )
    assert (
        Light.Entryway.autolight_entity_id
        == "automation.entryway_light_on_occupancy_or_door_open"
    )


def test_get_status(mock_client):
    mock_client.get_entity_status.side_effect = [
        {"state": "on", "attributes": {"brightness": 255, "color_temp": 300}},
        {"state": "on"},
    ]

    status = Light.LivingRoom.get_status()

    assert status == {
        "status": "on",
        "brightness": 255,
        "color_temp": 300,
        "autolight_status": "on",
    }
    mock_client.get_entity_status.assert_any_call("light.living_room")
    mock_client.get_entity_status.assert_any_call(
        "automation.living_room_lights_on_occupancy"
    )


def test_run_status(mock_client, capsys):
    mock_client.get_entity_status.side_effect = [
        {"state": "off", "attributes": {}},
        {"state": "on"},
    ]

    Light.Kitchen.run(LightCommand.STATUS)

    captured = capsys.readouterr()
    assert (
        "{'status': 'off', 'brightness': None, 'color_temp': None, 'autolight_status': 'on'}"
        in captured.out
    )


def test_run_enable_autolights(mock_client):
    Light.Bedroom.run(LightCommand.ENABLE_AUTOLIGHTS)

    mock_client.command_service.assert_called_once_with(
        "automation", "turn_on", {"entity_id": "automation.bedroom_lights_on_occupancy"}
    )


def test_run_disable_autolights(mock_client):
    Light.DiningRoom.run(LightCommand.DISABLE_AUTOLIGHTS)

    mock_client.command_service.assert_called_once_with(
        "automation",
        "turn_off",
        {"entity_id": "automation.kitchen_dining_automated_lights"},
    )


def test_run_light_command(mock_client):
    Light.Entryway.run(LightCommand.ON)

    mock_client.command_service.assert_called_once_with(
        "light", "turn_on", {"entity_id": "light.entryway"}
    )


def test_on_off_toggle_methods(mock_client):
    Light.LivingRoom.on()
    mock_client.command_service.assert_called_with(
        "light", "turn_on", {"entity_id": "light.living_room"}
    )

    Light.LivingRoom.off()
    mock_client.command_service.assert_called_with(
        "light", "turn_off", {"entity_id": "light.living_room"}
    )

    Light.LivingRoom.toggle()
    mock_client.command_service.assert_called_with(
        "light", "toggle", {"entity_id": "light.living_room"}
    )
