import enum

from commandable import Commandable

from .client import client


class SpeakerCommand(enum.Enum):
    PLAY = "play"
    PAUSE = "pause"

    @property
    def homeassistant_commandstr(self):
        return {
            SpeakerCommand.PLAY: "media_play",
            SpeakerCommand.PAUSE: "media_pause",
        }[self]


class Speaker(Commandable[SpeakerCommand], enum.Enum):
    LivingRoom = "living_room"
    DiningRoom = "dining_room"
    Kitchen = "kitchen"
    Office = "office"

    @property
    def entity_id(self):
        return f"media_player.{self.value}"

    def run(self, command: SpeakerCommand):
        client.__call__(
            "media_player",
            command.homeassistant_commandstr,
            {"entity_id": self.entity_id},
        )
