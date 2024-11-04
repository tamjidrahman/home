import concurrent.futures
import itertools
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

    @property
    def name(self) -> str:
        """Name of entity"""
        return self.entity_id

    def status(self, verbose: bool = False) -> dict:
        """
        Get state of the entity
        """
        return client.get_entity_status(self.entity_id)

    def get_commands(self) -> Iterable[Callable]:
        for methodname in self.__dir__():
            if methodname == "get_commands":
                continue
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
            commandable.name: commandable for commandable in self.commandables
        }

    def ClickChoiceType(self):
        return ChoiceType(self.choice_map)

    @property
    def entity_id(self) -> str:
        return ",".join(commandable.entity_id for commandable in self.commandables)

    def group_commands(self) -> Iterable[Callable]:
        return []

    def get_commands(self) -> Iterable[Callable]:
        commandable_name = type(self.commandables[0]).__name__.lower()
        commands = []

        # use a factory function to capture new functions in a loop
        # https://stackoverflow.com/questions/1107210/python-create-function-in-a-loop-capturing-the-loop-variable
        def cmdfnfactory(commandname):
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
                ] = [],
                *args,
                **kwargs,
            ):
                if not commandables:
                    commandables = self.commandables

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = {
                        executor.submit(
                            commandable.__getattribute__(commandname),
                            *args,
                            **kwargs,
                        ): commandable.name
                        for commandable in commandables
                    }
                    return {
                        futures[future]: future.result()
                        for future in concurrent.futures.as_completed(futures)
                    }

            commandfn.__name__ = commandname
            return commandfn

        for commandname in [
            command.__name__ for command in self.commandables[0].get_commands()
        ]:
            if commandname == "get_commands":
                continue
            commands.append(cmdfnfactory(commandname))

        return itertools.chain(self.group_commands(), commands)
