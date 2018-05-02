from typing import *
from weakref import WeakSet

ParameterType = TypeVar("ParameterType")
Action = Callable[[ParameterType], None]


class EventDelegate(Callable[[ParameterType], None]):
    def __init__(self, name: str):
        self.name = name
        self.actions: (Set[Action[ParameterType]]) = WeakSet()

    def add(self, *actions: Action[ParameterType]):
        self.actions.update(actions)

    def remove(self, *actions: Action[ParameterType]):
        self.actions.difference_update(actions)

    def __call__(self, content: ParameterType) -> None:
        print("Event:{} Content:{}".format(self.name, content))
        for callback in self.actions:
            callback(content)

    def __iadd__(self, other: "EventDelegate[ParameterType]"):
        self.add(other)
