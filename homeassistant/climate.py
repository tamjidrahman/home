from homeassistant.client import client


class Climate:

    @staticmethod
    def set(temperature: float):
        client.__call__(
            "climate",
            "set_temperature",
            {
                "entity_id": "climate.nest_learning_thermostat_4th_gen_thermostat",
                "temperature": temperature,
            },
        )

    @staticmethod
    def state() -> dict:
        raw_state = client.get_entity_state(
            "climate.nest_learning_thermostat_4th_gen_thermostat"
        )

        state = {
            "temperature": raw_state["attributes"]["current_temperature"],
            "target_temperature": raw_state["attributes"]["temperature"],
            "mode": raw_state["state"],
        }

        print(state)

        return state
