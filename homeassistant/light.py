import enum

from commandable import Commandable
from homeassistant import client


class LightCommand(enum.Enum):
    TOGGLE = "toggle"
    ON = "on"
    OFF = "off"
    STATUS = "status"
    DISABLE_AUTOLIGHTS = "disable_autolight"
    ENABLE_AUTOLIGHTS = "enable_autolight"

    @property
    def homeassistant_commandstr(self):
        return {
            LightCommand.TOGGLE: "toggle",
            LightCommand.ON: "turn_on",
            LightCommand.OFF: "turn_off",
        }[self]


class Light(Commandable[LightCommand], enum.Enum):
    LivingRoom = "living_room"
    Kitchen = "kitchen"
    DiningRoom = "dining_room"
    Bedroom = "bedroom"
    Entryway = "entryway"

    @property
    def entity_id(self):
        return f"light.{self.value}"

    @property
    def autolight_entity_id(self):
        # kitchen and dining shares autolights
        default = f"automation.{self.value}_lights_on_occupancy"
        return {
            Light.Kitchen: "automation.kitchen_dining_automated_lights",
            Light.DiningRoom: "automation.kitchen_dining_automated_lights",
            Light.Entryway: "automation.entryway_light_on_occupancy_or_door_open",
        }.get(self, default)

    def get_status(self):
        raw_status = client.get_entity_status(self.entity_id)
        status = {
            "status": raw_status["state"],
            "brightness": raw_status["attributes"].get("brightness"),
            "color_temp": raw_status["attributes"].get("color_temp"),
        }

        autolight_status = client.get_entity_status(self.autolight_entity_id)
        status["autolight_status"] = autolight_status["state"]

        return status

    def run(self, command: LightCommand):
        if command == LightCommand.STATUS:
            print(self.get_status())
            return

        if command == LightCommand.ENABLE_AUTOLIGHTS:
            client.__call__(
                "automation", "turn_on", {"entity_id": self.autolight_entity_id}
            )
            return

        if command == LightCommand.DISABLE_AUTOLIGHTS:
            client.__call__(
                "automation", "turn_off", {"entity_id": self.autolight_entity_id}
            )
            return

        client.__call__(
            "light", command.homeassistant_commandstr, {"entity_id": self.entity_id}
        )

    def on(self):
        self.run(LightCommand.ON)

    def off(self):
        self.run(LightCommand.OFF)

    def toggle(self):
        self.run(LightCommand.TOGGLE)
