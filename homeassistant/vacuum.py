import enum

import homeassistant.client as client
from homeassistant.commandable import Commandable

status = client.get_entity_status("vacuum.x40_ultra")
map = status["attributes"]["rooms"]["Map 1"]

names = {}
room_ids = {}

for room in map:
    names[room["name"]] = room["name"]
    room_ids[room["name"]] = room["id"]
Room = enum.Enum("Room", names)


class Vacuum(Commandable):

    def __init__(self, entity_id: str):
        self._entity_id = entity_id
        self.segments = {
            "kitchen": 6,
        }

    @property
    def entity_id(self) -> str:
        return self._entity_id

    def status(self, verbose: bool = False) -> dict:
        """Get status of the vacuum."""

        raw_status = client.get_entity_status(self.entity_id)

        if verbose:
            return raw_status

        status = {
            "status": raw_status["state"],
        }

        return status

    def start(self):
        """Start the vacuum."""
        client.command_service("vacuum", "start", {"entity_id": self.entity_id})

    def stop(self):
        """Stop the vacuum."""
        client.command_service("vacuum", "stop", {"entity_id": self.entity_id})

    def clean_room(self, rooms: list[Room]):
        """Clean the specified rooms."""
        client.command_service(
            "dreame_vacuum",
            "vacuum_clean_segment",
            {
                "entity_id": self.entity_id,
                "segments": [room_ids[room.value] for room in rooms],
            },
        )
