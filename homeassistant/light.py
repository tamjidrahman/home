import enum

from commandable import Commandable
from homeassistant.client import client


class LightCommand(enum.Enum):
    TOGGLE = "toggle"
    ON = "on"
    OFF = "off"
    STATE = "state"
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

    def get_state(self):
        raw_state = client.get_entity_state(self.entity_id)
        state = {
            "state": raw_state["state"],
            "brightness": raw_state["attributes"].get("brightness"),
            "color_temp": raw_state["attributes"].get("color_temp"),
        }

        autolight_state = client.get_entity_state(self.autolight_entity_id)
        state["autolight_state"] = autolight_state["state"]

        return state

    def run(self, command: LightCommand):
        if command == LightCommand.STATE:
            print(self.get_state())
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
