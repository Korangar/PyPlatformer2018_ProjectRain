from typing import *
from weakref import WeakSet

_Content = TypeVar("_Content")


class Observer(Generic[_Content]):
    def __init__(self, name: str):
        self.name = name
        self.observers: Set[Callable[[_Content], None]] = WeakSet()

    def observe(self, *callback: Callable[[_Content], None]):
        self.observers.update(callback)

    def remove(self, *callback: Callable[[_Content], None]):
        self.observers.difference_update(callback)

    def __call__(self, content: _Content):
        print("Observer triggered! Event:{} Content:{}".format(self.name, content))
        for callback in self.observers:
            callback(content)
