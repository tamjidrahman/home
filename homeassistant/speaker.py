import enum
import json

from commandable import Commandable
from homeassistant import client


class SpeakerCommand(enum.Enum):
    PLAY = "play"
    PAUSE = "pause"
    STATUS = "status"

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

    @classmethod
    def get_status_all(cls):
        return {item.entity_id: item.get_status() for item in cls}

    def get_status(self):
        raw_status = client.get_entity_status(self.entity_id)
        status = {
            "status": raw_status["state"],
            "media_title": raw_status["attributes"].get("media_title"),
            "media_artist": raw_status["attributes"].get("media_artist"),
            "media_album_name": raw_status["attributes"].get("media_album_name"),
            "media_playlist": raw_status["attributes"].get("media_playlist"),
        }
        return status

    def run(self, command: SpeakerCommand):
        if command == SpeakerCommand.STATUS:
            print(json.dumps(self.get_status()))
            return
        client.command_service(
            "media_player",
            command.homeassistant_commandstr,
            {"entity_id": self.entity_id},
        )
