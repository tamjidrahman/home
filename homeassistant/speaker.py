from typing import Callable, Iterable
from homeassistant import client
from homeassistant.commandable import Commandable, CommandableGroup


class Speaker(Commandable):
    def __init__(self, entity_id):
        self._entity_id = entity_id

    @property
    def entity_id(self):
        return self._entity_id

    @property
    def name(self):
        # override readable name to exclude "media_player." prefix
        return self._entity_id[len("media_player.") :]

    def status(self, verbose: bool = False):
        """Get status of the speaker."""
        raw_status = client.get_entity_status(self.entity_id)

        if verbose:
            return raw_status

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
        """Play media on the speaker."""
        self.__run("media_play")

    def pause(self):
        """Pause media on the speaker."""
        self.__run("media_pause")


class SpeakerGroup(CommandableGroup):
    def join_speakers(self):
        """Enable sleep mode for adaptive lighting"""
        return client.command_service(
            "script",
            "turn_on",
            {"entity_id": "script.join_speakers"},
        )

    def unjoin_speakers(self):
        """Disable sleep mode for adaptive lighting"""
        return client.command_service(
            "script",
            "turn_on",
            {"entity_id": "script.unjoin_speakers"},
        )

    def group_commands(self) -> Iterable[Callable]:
        return [self.join_speakers, self.unjoin_speakers]
