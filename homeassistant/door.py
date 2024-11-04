from typing import Optional

from homeassistant import client
from homeassistant.commandable import Commandable


class Door(Commandable):
    def __init__(self, entity_id: str, lock_id: Optional[str] = None):
        self._entity_id = entity_id
        self.lock_id = lock_id

    @property
    def entity_id(self) -> str:
        return self._entity_id

    @property
    def name(self) -> str:
        return self.entity_id[len("binary_sensor.") : -len("_sensor")]

    def status(self, verbose: bool = False):
        raw_status = client.get_entity_status(self.entity_id)
        if self.lock_id:
            raw_status["lock_status"] = client.get_entity_status(self.lock_id)

        if verbose:
            return raw_status

        status = {
            "state": "closed" if raw_status["state"] == "off" else "open",
        }

        if self.lock_id:
            status["lock_status"] = raw_status["lock_status"]["state"]

        return status
