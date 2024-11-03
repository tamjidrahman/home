import enum
from abc import abstractmethod
from typing import Generic, TypeVar

C = TypeVar("C", bound=enum.Enum)


class Commandable(Generic[C]):

    @property
    @abstractmethod
    def entity_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def run(self, command: C):
        raise NotImplementedError
