import typer

from homeassistant.commandable import CommandableGroup
from homeassistant.light import Light
from homeassistant.speaker import Speaker
from homeassistant.thermostat import Thermostat

app = typer.Typer()

""" Light V2"""
light_app = typer.Typer(name="light")
lightgroup = CommandableGroup(
    [
        Light("light.living_room", "automation.kitchen_dining_automated_lights"),
        Light("light.kitchen", "automation.kitchen_dining_automated_lights"),
        Light("light.dining_room", "automation.kitchen_dining_automated_lights"),
        Light("light.bedroom", "automation.entryway_light_on_occupancy_or_door_open"),
        Light("light.entryway", "automation.entryway_light_on_occupancy_or_door_open"),
    ]
)

for command in lightgroup.get_commands():
    light_app.command()(command)

app.add_typer(light_app)

""" Speaker V2"""
speaker_app = typer.Typer(name="speaker")

speakergroup = CommandableGroup(
    [
        Speaker("media_player.living_room"),
        Speaker("media_player.dining_room"),
        Speaker("media_player.kitchen"),
        Speaker("media_player.office"),
    ]
)


for command in speakergroup.get_commands():
    speaker_app.command()(command)

app.add_typer(speaker_app)

""" Themostat V2"""
thermostat_app = typer.Typer(name="thermostat")

thermostat = Thermostat()
for command in thermostat.get_commands():
    thermostat_app.command(command.__name__)(command)


app.add_typer(thermostat_app)


if __name__ == "__main__":
    app()
