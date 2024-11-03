from homeassistant import client


class Climate:

    @staticmethod
    def set(temperature: float):
        client.command_service(
            "climate",
            "set_temperature",
            {
                "entity_id": "climate.nest_learning_thermostat_4th_gen_thermostat",
                "temperature": temperature,
            },
        )

    @staticmethod
    def status() -> dict:
        raw_status = client.get_entity_status(
            "climate.nest_learning_thermostat_4th_gen_thermostat"
        )

        status = {
            "temperature": raw_status["attributes"]["current_temperature"],
            "target_temperature": raw_status["attributes"]["temperature"],
            "mode": raw_status["state"],
        }

        print(status)

        return status
