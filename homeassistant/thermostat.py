from homeassistant import client
from homeassistant.commandable import Commandable


class Thermostat(Commandable):

    def __init__(self, entity_id):
        self._entity_id = entity_id

    @property
    def entity_id(self):
        return self._entity_id

    def set(self, temperature: float):
        return client.command_service(
            "climate",
            "set_temperature",
            {
                "entity_id": self.entity_id,
                "temperature": temperature,
            },
        )

    def status(self, verbose: bool = False) -> dict:
        raw_status = client.get_entity_status(self.entity_id)

        if verbose:
            return raw_status

        status = {
            "temperature": raw_status["attributes"]["current_temperature"],
            "target_temperature": raw_status["attributes"]["temperature"],
            "mode": raw_status["state"],
        }

        return status
