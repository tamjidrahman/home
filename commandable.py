import enum
from abc import abstractmethod
from typing import Generic, TypeVar, get_args

C = TypeVar("C", bound=enum.Enum)


class Commandable(Generic[C]):

    @abstractmethod
    def run(self, command: C):
        raise NotImplementedError

    @classmethod
    def get_command_type(cls):
        if hasattr(cls, "__orig_bases__"):
            return get_args(cls.__orig_bases__[0])[0]
        return C
