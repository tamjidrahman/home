from homeassistant import client
from homeassistant.commandable import Commandable


class Speaker(Commandable):

    def __init__(self, entity_id):
        self._entity_id = entity_id

    @property
    def entity_id(self):
        return self._entity_id

    def status(self, verbose: bool = False):
        raw_status = client.get_entity_status(self.entity_id)
        status = {
            "status": raw_status["state"],
            "media_title": raw_status["attributes"].get("media_title"),
            "media_artist": raw_status["attributes"].get("media_artist"),
            "media_album_name": raw_status["attributes"].get("media_album_name"),
            "media_playlist": raw_status["attributes"].get("media_playlist"),
        }
        return status

    def __run(self, command: str):
        client.command_service(
            "media_player",
            command,
            {"entity_id": self.entity_id},
        )

    def play(self):
        self.__run("media_play")

    def pause(self):
        self.__run("media_pause")
