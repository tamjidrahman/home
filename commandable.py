import enum
from abc import abstractmethod
from typing import Generic, TypeVar

C = TypeVar("C", bound=enum.Enum)


class Commandable(Generic[C]):

    @abstractmethod
    def run(self, command: C):
        raise NotImplementedError
