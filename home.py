import json
from functools import wraps
from pathlib import Path

import toml
import typer

from homeassistant.commandable import CommandableGroup
from homeassistant.light import Light, LightGroup
from homeassistant.speaker import Speaker
from homeassistant.thermostat import Thermostat
from homeassistant.vacuum import Vacuum

app = typer.Typer()


def cli_wrapper(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)

        if ret is not None:
            typer.echo(json.dumps(ret))

        return ret

    return wrapper


def load_config(config_file=Path.home() / ".config/home/config.toml"):
    config_path = Path(config_file)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file {config_file} not found.")
    return toml.load(config_path)


config = load_config()

""" Light"""
light_app = typer.Typer(name="light", help="Light commands")
lightgroup = LightGroup(
    [Light(light["entity_id"], light["automation"]) for light in config["lights"]]
)

for command in map(cli_wrapper, lightgroup.get_commands()):
    light_app.command()(command)

app.add_typer(light_app)

""" Speaker"""
speaker_app = typer.Typer(name="speaker", help="Speaker commands")

speakergroup = CommandableGroup(
    [Speaker(speaker["entity_id"]) for speaker in config["speakers"]]
)


for command in map(cli_wrapper, speakergroup.get_commands()):
    speaker_app.command()(command)

app.add_typer(speaker_app)

""" Thermostat"""
thermostat_app = typer.Typer(name="thermostat", help="Thermostat commands")

thermostat = Thermostat(config["thermostat"]["entity_id"])
for command in map(cli_wrapper, thermostat.get_commands()):
    thermostat_app.command(command.__name__)(command)


app.add_typer(thermostat_app)


""" Vacuum"""
vacuum_app = typer.Typer(name="vacuum", help="Vacuum commands")

vacuum = Vacuum(config["vacuum"]["entity_id"])
for command in map(cli_wrapper, vacuum.get_commands()):
    vacuum_app.command(command.__name__)(command)


app.add_typer(vacuum_app)

if __name__ == "__main__":
    app()
