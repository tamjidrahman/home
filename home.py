import json

import typer

from homeassistant.climate import Climate
from homeassistant.light import Light
from homeassistant.speaker import Speaker

app = typer.Typer()

"""
Generate a command line interface for each commandable class
"""
for i, commandable_class in enumerate([Speaker, Light]):
    commandable_class_app = typer.Typer(name=commandable_class.__name__.lower())
    for commandable in commandable_class:
        commandable_class_app.command(commandable.value)(commandable.run)

    status_command = lambda i=i: print(  # loops do not create closures, so set a dummy default (i) to force variable capture
        json.dumps(
            {
                commandable.entity_id: commandable.get_status()
                for commandable in commandable_class
            }
        )
    )

    commandable_class_app.command("status")(status_command)

    app.add_typer(commandable_class_app)


"""
Generate a command line interface for the climate class
"""
climate_app = typer.Typer(name="climate")

for method in Climate.__dict__.values():
    if callable(method) and not method.__name__.startswith("__"):
        climate_app.command()(method)

app.add_typer(climate_app)

if __name__ == "__main__":
    app()
