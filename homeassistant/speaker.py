import enum

from commandable import Commandable
from homeassistant.client import client


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

    def get_status(self):
        raw_status = client.get_entity_status(self.entity_id)
        print(raw_status)
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
            print(self.get_status())
            return
        client.__call__(
            "media_player",
            command.homeassistant_commandstr,
            {"entity_id": self.entity_id},
        )
