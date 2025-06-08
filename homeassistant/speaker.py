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
        """Execute a media player command on the speaker."""
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

    def next(self):
        """Play next track on the speaker."""
        self.__run("media_next_track")

    def previous(self):
        """Play next track on the speaker."""
        self.__run("media_previous_track")

    def stop(self):
        """Play next track on the speaker."""
        self.__run("media_stop")

    def volume_up(self):
        """Raise volume of the speaker."""
        self.__run("volume_up")

    def volume_down(self):
        """Lower volume of the speaker."""
        self.__run("volume_down")

    def volume_set(self, volume: int):
        """Set volume of the speaker."""
        return client.command_service(
            "media_player",
            "volume_set",
            {
                "entity_id": self.entity_id,
                "volume_level": volume / 100,
            },
        )

    def volume_mute(self, mute: bool = True):
        """Mute or unmute the speaker.

        Args:
            mute: True to mute, False to unmute. Defaults to True.
        """
        return client.command_service(
            "media_player",
            "volume_mute",
            {
                "entity_id": self.entity_id,
                "is_volume_muted": mute,
            },
        )


class SpeakerGroup(CommandableGroup):
    def join_speakers(self):
        """Join speakers"""
        return client.command_service(
            "script",
            "turn_on",
            {"entity_id": "script.join_speakers"},
        )

    def unjoin_speakers(self):
        """Unjoin speakers"""
        return client.command_service(
            "script",
            "turn_on",
            {"entity_id": "script.unjoin_speakers"},
        )

    def group_commands(self) -> Iterable[Callable]:
        return [self.join_speakers, self.unjoin_speakers]
