import typer

from homeassistant.light import Light
from homeassistant.speaker import Speaker

app = typer.Typer()

"""
Generate a command line interface for each commandable class
"""
for commandable_class in [Light, Speaker]:
    commandable_class_app = typer.Typer(name=commandable_class.__name__.lower())
    for commandable in commandable_class:
        commandable_class_app.command(commandable.value)(commandable.run)

    app.add_typer(commandable_class_app)


if __name__ == "__main__":
    app()
