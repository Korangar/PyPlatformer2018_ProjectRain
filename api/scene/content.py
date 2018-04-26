from ..utilities.geometry import Point
from ..events.observer import Observer

from .scene_object import SceneObject

from typing import *


class SceneContent:
    def __init__(self, position=Point(0, 0)):
        self._tags: Set[str] = set()
        self.scene: SceneObject = None
        self.position: Point = position
        name = type(self).__name__
        self.on_spawn: Observer[SceneContent] = Observer("{} spawned!".format(name))
        self.on_erase: Observer[SceneContent] = Observer("{} erased!".format(name))

    def __repr__(self) -> str:
        return "<{}@{}>".format(super().__repr__(), self.scene)

    def get_tags(self) -> Set[str]:
        return self._tags


class Agent(SceneContent):
    def __init__(self, position=Point(0, 0)):
        super().__init__(position)

    def update_agency(self, delta_time: float) -> None:
        pass


class Player(Agent):
    def __init__(self, position=Point(0, 0)):
        super().__init__(position)

    def update_will(self, delta_time: float) -> None:
        pass
