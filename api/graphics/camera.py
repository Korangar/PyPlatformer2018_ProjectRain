from ..utilities.geometry import Point
from ..utilities.vector import v_add
from ..scene.content import SceneContent

from .projection import Projection, calculate_anchor
from .component import AutoGraphicsComponent
from .drawing import Surface

from typing import *


RenderTarget = Surface


class Camera(SceneContent):
    def __init__(self, position: Point, cam_id: str, render_target: RenderTarget,
                 rel_anchor: Tuple[float, float]=(0.5, 0.5),
                 pixels_per_tile: int=32,
                 inverse_h: bool=False,
                 inverse_v: bool=True):
        super().__init__(position)
        self.projection = Projection(anchor=calculate_anchor(rel_anchor, render_target.get_size(), pixels_per_tile),
                                     dimension=render_target.get_size(),
                                     pixels_per_tile=pixels_per_tile,
                                     inverse_h=inverse_h,
                                     inverse_v=inverse_v)
        self.render_target = render_target
        self.cam_id = cam_id

    def in_view(self, p: Point) -> bool:
        return self.projection.in_view(p, self.position)

    def screen_point(self, p: Point) -> Tuple[int, int]:
        x, y = p
        dx, dy = self.projection.dimension
        return (x+dx) % dx, (y+dy) % dy

    def view_origin(self):
        return v_add(self.position, self.projection.anchor)

    def project(self, p: Point) -> Point:
        return self.projection.project(p, self.position)

    def render(self, components: Iterable[AutoGraphicsComponent]):
        for c in components:
            c.draw(self)
