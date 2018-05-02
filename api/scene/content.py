from ..utilities.geometry import Point
from .scene_object import SceneObject
from typing import *


class SceneContent:
    # todo clear timing related stuff on scene change

    def __init__(self, position=Point(0, 0)):
        self.scene: SceneObject = None
        self._tags: Set[str] = set()
        self.position: Point = position

    def __repr__(self) -> str:
        return "<{}@{}>".format(super().__repr__(), self.scene)

    def get_tags(self) -> Set[str]:
        return self._tags

    def get_scene_time(self) -> float:
        return self.scene.current_time

    def spawn(self):
        pass

    def destroy(self):
        pass


class Actor(SceneContent):
    def __init__(self, position=Point(0, 0)):
        super().__init__(position)

    def update(self) -> None:
        pass
