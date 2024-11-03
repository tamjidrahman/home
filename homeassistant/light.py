import enum

from commandable import Commandable

from .client import client


class LightCommand(enum.Enum):
    TOGGLE = "toggle"
    ON = "on"
    OFF = "off"

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

    def run(self, command: LightCommand):
        client.__call__(
            "light", command.homeassistant_commandstr, {"entity_id": self.entity_id}
        )

    def on(self):
        self.run(LightCommand.ON)

    def off(self):
        self.run(LightCommand.OFF)

    def toggle(self):
        self.run(LightCommand.TOGGLE)
