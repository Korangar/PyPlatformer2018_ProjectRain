from typing import *

ParameterType = TypeVar("ParameterType")
Action = Callable[[ParameterType], None]


class EventDelegate(Callable[[ParameterType], None]):
    def __init__(self, name: str, verbose=False):
        self.name = name
        self.verbose = verbose
        self.actions: (Set[Action[ParameterType]]) = set()

    def add(self, *actions: Action[ParameterType]):
        self.actions.update(actions)

    def remove(self, *actions: Action[ParameterType]):
        self.actions.difference_update(actions)

    def __call__(self, content: ParameterType) -> None:
        if self.verbose:
            print(self.name, content)
        for callback in self.actions:
            callback(content)

    def __iadd__(self, other: "EventDelegate[ParameterType]"):
        self.add(other)
        return self
