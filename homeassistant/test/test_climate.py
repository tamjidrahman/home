import unittest
from unittest.mock import patch

from homeassistant.climate import Climate


class TestClimate(unittest.TestCase):

    @patch("homeassistant.client.command_service")
    def test_set_temperature(self, mock_command_service):
        Climate.set(22.5)
        mock_command_service.assert_called_once_with(
            "climate",
            "set_temperature",
            {
                "entity_id": "climate.nest_learning_thermostat_4th_gen_thermostat",
                "temperature": 22.5,
            },
        )

    @patch("homeassistant.client.get_entity_status")
    def test_status(self, mock_get_entity_status):
        mock_get_entity_status.return_value = {
            "state": "heat",
            "attributes": {
                "current_temperature": 21.0,
                "temperature": 22.0,
            },
        }

        with patch("builtins.print") as mock_print:
            result = Climate.status()

        expected_status = {
            "temperature": 21.0,
            "target_temperature": 22.0,
            "mode": "heat",
        }

        self.assertEqual(result, expected_status)
        mock_print.assert_called_once_with(expected_status)
        mock_get_entity_status.assert_called_once_with(
            "climate.nest_learning_thermostat_4th_gen_thermostat"
        )
