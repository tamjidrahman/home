from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from typing import Annotated

import click
import typer

from homeassistant import client
from homeassistant.merge_args import merge_args


class Commandable(ABC):
    """
    An abstract base class for commandable entities in Home Assistant.
    """

    @property
    @abstractmethod
    def entity_id(self) -> str:
        """
        Abstract property that should return the entity ID.
        """
        pass

    def status(self, verbose: bool = False) -> dict:
        """
        Get state of the entity
        """
        return client.get_entity_status(self.entity_id)

    def get_commands(self) -> Iterable[Callable]:
        for methodname in self.__dir__():
            method = self.__getattribute__(methodname)
            if (
                callable(method)
                and not methodname.startswith("__")
                and not methodname.startswith("_")
            ):
                yield method


class ChoiceType(click.Choice):
    def __init__(self, typemap):
        super(ChoiceType, self).__init__(typemap.keys())
        self.typemap = typemap

    def convert(self, value, param, ctx):
        value = super(ChoiceType, self).convert(value, param, ctx)
        return self.typemap[value]


class CommandableGroup(Commandable, ABC):
    """
    An abstract base class for commandable groups in Home Assistant.
    """

    def __init__(self, commandables: list[Commandable]):
        self.commandables = commandables
        self.choice_map = {
            commandable.entity_id: commandable for commandable in self.commandables
        }

    def ClickChoiceType(self):
        return ChoiceType(self.choice_map)

    @property
    def entity_id(self) -> str:
        return ",".join(commandable.entity_id for commandable in self.commandables)

    def status(self, verbose: bool = False) -> dict:
        return {
            commandable.entity_id: commandable.status(verbose=verbose)
            for commandable in self.commandables
        }

    def get_commands(self) -> Iterable[Callable]:
        commandable_name = type(self.commandables[0]).__name__.lower()
        for commandname in [
            command.__name__ for command in self.commandables[0].get_commands()
        ]:
            if commandname == "get_commands":
                continue

            reference_method = self.commandables[0].__getattribute__(commandname)

            @merge_args(reference_method, drop_args=["self"])
            def commandfn(
                commandables: Annotated[
                    list[Commandable],
                    typer.Option(
                        f"-{commandable_name[0]}",
                        f"--{commandable_name}",
                        click_type=self.ClickChoiceType(),
                    ),
                ],
                commandname=commandname,  # set default commandname to force variable capture in list
                *args,
                **kwargs,
            ):
                for commandable in commandables:
                    commandable.__getattribute__(commandname)(*args, **kwargs)

            commandfn.__name__ = commandname

            yield commandfn