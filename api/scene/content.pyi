from ..utilities.geometry import Point
from ..events.observer import Observer

from .scene_object import SceneObject

from typing import *

class SceneContent:
    _tags: Sequence[str]
    scene: SceneObject
    position: Point
    children: List[SceneContent]
    on_spawn: Observer[SceneContent]
    on_erase: Observer[SceneContent]
    def __init__(self, position: Point=Point(0, 0)) -> None: ...

    def get_tags(self) -> Sequence[str]: ...


class Agent(SceneContent):
    def __init__(self, position: Point=(0, 0)) -> None: ...

    def update_agency(self, delta_time: float): ...


class Player(Agent):
    def __init__(self, position: Point=(0, 0)) -> None: ...

    def update_will(self, delta_time: float) -> None: ...