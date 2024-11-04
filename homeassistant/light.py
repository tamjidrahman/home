from homeassistant import client
from homeassistant.commandable import Commandable, CommandableGroup


class Light(Commandable):

    def __init__(self, entity_id, autolight_entity_id):
        self._entity_id = entity_id
        self.autolight_entity_id = autolight_entity_id

    @property
    def entity_id(self):
        return self._entity_id

    def status(self, verbose: bool = False):
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
        client.command_service("light", "toggle", {"entity_id": self.entity_id})

    def on(self):
        client.command_service("light", "turn_on", {"entity_id": self.entity_id})

    def off(self):
        client.command_service("light", "turn_off", {"entity_id": self.entity_id})

    def enable_autolights(self):
        client.command_service(
            "automation", "turn_on", {"entity_id": self.autolight_entity_id}
        )

    def disable_autolights(self):
        client.command_service(
            "automation", "turn_off", {"entity_id": self.autolight_entity_id}
        )

    def __str__(self):
        return self.entity_id
