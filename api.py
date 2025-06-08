import json
from pathlib import Path
from fastapi import FastAPI, Query
import toml
from fastapi.middleware.cors import CORSMiddleware

from homeassistant.commandable import CommandableGroup
from homeassistant.door import Door
from homeassistant.light import Light, LightGroup
from homeassistant.speaker import Speaker, SpeakerGroup
from homeassistant.thermostat import Thermostat
from homeassistant.vacuum import Vacuum

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL (Next.js dev server)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc)
    allow_headers=["*"],  # Allow all headers (e.g. Authorization, Content-Type)
)


def load_config(config_file=Path.home() / ".config/home/config.toml"):
    config_path = Path(config_file)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file {config_file} not found.")
    return toml.load(config_path)


config = load_config()


def register_routes(entity_name: str, devices, app: FastAPI):
    device_lookup = {device.name: device for device in devices}
    commands = [cmd.__name__ for cmd in devices[0].get_commands()]  # assume uniform

    # Register the commands endpoint
    @app.get(f"/{entity_name}/commands")
    def get_commands():
        return commands

    # Register each command route
    for cmd_name in commands:
        route = f"/{entity_name}/{cmd_name}"

        def make_handler(cmd):
            def handler(names: list[str] | None = Query(None, alias=entity_name)):
                selected = (
                    [device_lookup[name] for name in names if name in device_lookup]
                    if names
                    else device_lookup.values()
                )
                return {
                    device.name: getattr(device, cmd.__name__)() for device in selected
                }

            return handler

        method = app.get if cmd_name == "status" else app.post
        method(route)(make_handler(getattr(devices[0], cmd_name)))


""" Lights """
lights = [Light(light["entity_id"], light["automation"]) for light in config["lights"]]
register_routes("light", lights, app)

""" Speakers """
speakers = [Speaker(s["entity_id"]) for s in config["speakers"]]
register_routes("speaker", speakers, app)

""" Thermostat """
thermostats = [Thermostat(config["thermostat"]["entity_id"])]
register_routes("thermostat", thermostats, app)

""" Vacuum """
vacuums = [Vacuum(config["vacuum"]["entity_id"])]
register_routes("vacuum", vacuums, app)

""" Doors """
doors = [Door(d["entity_id"], lock_id=d.get("lock_id")) for d in config["doors"]]
register_routes("door", doors, app)
