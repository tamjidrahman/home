import json
import inspect
from pathlib import Path
from fastapi import FastAPI, Query, Request
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
    allow_origins=["*"],  # Frontend URL (Next.js dev server)
    allow_credentials=False,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc)
    allow_headers=["*"],  # Allow all headers (e.g. Authorization, Content-Type)
)


def load_config(config_file=Path.home() / ".config/home/config.toml"):
    config_path = Path(config_file)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file {config_file} not found.")
    return toml.load(config_path)


config = load_config()


from makefun import create_function, with_signature

def register_routes(entity_name: str, devices, app: FastAPI):
    device_lookup = {device.name: device for device in devices}
    commands = [cmd for cmd in devices[0].get_commands()]  # assume uniform

    @app.get(f"/{entity_name}/commands")
    def get_commands():
        return [cmd.__name__ for cmd in commands]

    for cmd in commands:
        cmd_name = cmd.__name__
        route = f"/{entity_name}/{cmd_name}"
        sig = inspect.signature(cmd)

        parameters = [
            inspect.Parameter(
                name="names",
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=Query(None, alias=entity_name),
                annotation=list[str] | None,
            )
        ]

        for name, param in sig.parameters.items():
            if name == "self":
                continue
            annotation = param.annotation if param.annotation is not inspect.Parameter.empty else str
            default = param.default if param.default is not inspect.Parameter.empty else ...
            parameters.append(
                inspect.Parameter(
                    name=name,
                    kind=inspect.Parameter.KEYWORD_ONLY,
                    default=Query(default),
                    annotation=annotation,
                )
            )

        new_sig = inspect.Signature(parameters)

        def make_logic(cmd):
            def logic(**kwargs):
                selected_names = kwargs.pop("names", None)
                selected = (
                    [device_lookup[name] for name in selected_names if name in device_lookup]
                    if selected_names else device_lookup.values()
                )
                result = {}
                for device in selected:
                    method = getattr(device, cmd.__name__)
                    result[device.name] = method(**kwargs)
                return result
            return logic

        logic_fn = make_logic(cmd)

        # ✅ Wrap with FastAPI-compatible signature
        handler = with_signature(new_sig)(logic_fn)

        method = app.get if cmd_name == "status" else app.post
        method(route)(handler)

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
