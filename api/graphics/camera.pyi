from ..scene.content import SceneContent
from ..utilities.projection import Projection
from ..utilities.geometry import Point

from ._pygame_drawing import Surface

from typing import *


class Camera :
    cam_id: str
    anchor: SceneContent
    view: Projection
    target: Surface
    ppt: int

    def __init__(self, cam_id:str, view: Projection, anchor: SceneContent, target: Surface, ppt: int): ...

    def is_in_view(self, point: Point) -> bool: ...

    def is_on_screen(self, point: Point) -> bool: ...

    def get_view_origin(self) -> Point: ...

    def get_screen_point(self, x: Union[int, float], y: Union[int, float]) -> Point: ...

    def project(self, point: Point) -> Point: ...
