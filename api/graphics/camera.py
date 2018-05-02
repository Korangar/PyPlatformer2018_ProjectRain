from ..utilities.geometry import Point
from ..utilities.vector import *
from ..scene.content import Actor, SceneContent

from .projection import Projection, calculate_anchor
from .component import AutoGraphicsComponent
from .drawing import Surface

from typing import *


RenderTarget = Surface


class Camera(Actor):
    def __init__(self, position: Point, cam_id: str, render_target: RenderTarget,
                 rel_anchor: Tuple[float, float]=(0.5, 0.5),
                 pixels_per_tile: int=32,
                 inverse_h: bool=False,
                 inverse_v: bool=True,
                 follow_target: SceneContent = None,
                 grid_locks_view: bool = False):

        super().__init__(position)
        self.projection = Projection(anchor=calculate_anchor(rel_anchor, render_target.get_size(), pixels_per_tile),
                                     dimension=render_target.get_size(),
                                     pixels_per_tile=pixels_per_tile,
                                     inverse_h=inverse_h,
                                     inverse_v=inverse_v)
        self.render_target = render_target
        self.cam_id = cam_id
        self.follow_target = follow_target
        self.grid_locks_view = grid_locks_view

    def in_view(self, p: Point) -> bool:
        return self.projection.in_view(p, self.position)

    def project(self, p: Point) -> Point:
        return self.projection.project(p, self.position)

    def view_origin(self):
        return self.projection.view_origin(self.position)

    def view_dimension(self):
        return self.projection.view_dimension()

    def view_rectangle(self):
        return self.projection.view_rectangle(self.position)

    def screen_point(self, p: Point) -> Tuple[int, int]:
        x, y = p
        dx, dy = self.projection.dimension
        return (x+dx) % dx, (y+dy) % dy

    def render(self, components: Iterable[AutoGraphicsComponent]):
        for c in components:
            c.draw(self)

    def update(self):
        if self.follow_target:
            self.position = self.follow_target.position
        if self.grid_locks_view:
            tg = self.scene.tile_grid
            grid = len(tg), len(tg[0])
            view = self.projection.view_rectangle(self.position)
            # adjustment to up right
            min_adj = v_max((0, 0), v_sub((0, 0), view.min()))
            # adjustment to down left
            max_adj = v_min((0, 0), v_sub(grid, view.max()))
            self.position = v_add(self.position, min_adj, max_adj)
