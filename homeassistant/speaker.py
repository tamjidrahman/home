import enum

from commandable import Commandable
from homeassistant.client import client


class SpeakerCommand(enum.Enum):
    PLAY = "play"
    PAUSE = "pause"
    STATE = "state"

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

    def get_state(self):
        raw_state = client.get_entity_state(self.entity_id)
        print(raw_state)
        state = {
            "state": raw_state["state"],
            "media_title": raw_state["attributes"].get("media_title"),
            "media_artist": raw_state["attributes"].get("media_artist"),
            "media_album_name": raw_state["attributes"].get("media_album_name"),
            "media_playlist": raw_state["attributes"].get("media_playlist"),
        }
        return state

    def run(self, command: SpeakerCommand):
        if command == SpeakerCommand.STATE:
            print(self.get_state())
            return
        client.__call__(
            "media_player",
            command.homeassistant_commandstr,
            {"entity_id": self.entity_id},
        )
