from typing import Callable, Iterable

from homeassistant import client
from homeassistant.commandable import Commandable, CommandableGroup


class Light(Commandable):
    def __init__(self, entity_id, autolight_entity_id):
        self._entity_id = entity_id
        self.autolight_entity_id = autolight_entity_id

    @property
    def entity_id(self):
        return self._entity_id

    @property
    def name(self):
        # override readable name to exclude "light." prefix
        return self._entity_id[len("light.") :]

    def status(self, verbose: bool = False):
        """
        Get the status of the light.

        Args:
            verbose (bool): If True, return the full status information.

        Returns:
            dict: The status of the light, including autolight status.
        """
        raw_status = client.get_entity_status(self.entity_id)

        autolight_status = client.get_entity_status(self.autolight_entity_id)

        raw_status["autolight_status"] = autolight_status["state"]

        if verbose:
            return raw_status

        status = {
            "status": raw_status["state"],
            "autolight_status": raw_status["autolight_status"],
            "brightness": raw_status["attributes"].get("brightness"),
            "color_temp": raw_status["attributes"].get("color_temp"),
        }

        return status

    def toggle(self):
        """
        Toggle the light on or off.

        Returns:
            dict: The result of the toggle command.
        """
        return client.command_service("light", "toggle", {"entity_id": self.entity_id})

    def on(self):
        """
        Turn on the light.

        Returns:
            dict: The result of the turn on command.
        """
        return client.command_service("light", "turn_on", {"entity_id": self.entity_id})

    def off(self):
        """
        Turn off the light.

        Returns:
            dict: The result of the turn off command.
        """
        return client.command_service(
            "light", "turn_off", {"entity_id": self.entity_id}
        )

    def enable_autolights(self):
        """
        Enable autolights for this light.

        Returns:
            dict: The result of enabling autolights.
        """
        return client.command_service(
            "automation", "turn_on", {"entity_id": self.autolight_entity_id}
        )

    def disable_autolights(self):
        """
        Disable autolights for this light.

        Returns:
            dict: The result of disabling autolights.
        """
        return client.command_service(
            "automation", "turn_off", {"entity_id": self.autolight_entity_id}
        )

    def __str__(self):
        return self.entity_id


class LightGroup(CommandableGroup):
    def enable_sleepmode(self):
        """Enable sleep mode for adaptive lighting"""
        return client.command_service(
            "switch",
            "turn_on",
            {"entity_id": "switch.adaptive_lighting_sleep_mode_adaptive_lighting"},
        )

    def disable_sleepmode(self):
        """Disable sleep mode for adaptive lighting"""
        return client.command_service(
            "switch",
            "turn_off",
            {"entity_id": "switch.adaptive_lighting_sleep_mode_adaptive_lighting"},
        )

    def group_commands(self) -> Iterable[Callable]:
        return [self.enable_sleepmode, self.disable_sleepmode]
