from api.utilities.geometry import Point, Rectangle
from api.utilities.vector import *

from typing import *


class Projection(NamedTuple):
    anchor: Vector2
    dimension: Tuple[int, int]
    pixels_per_tile: int = 32
    inverse_v: bool = True
    inverse_h: bool = False

    def in_view(self, point: Point, view_offset: Vector2=(0, 0)) -> bool:
        return Rectangle(Point(0, 0), self.dimension).intersect(self.project(point, view_offset))

    def project(self, point: Point, view_offset: Vector2=Vector2(0, 0)) -> Point:
        view_origin = self.view_origin(view_offset)
        x, y = v_mul(v_sub(point, view_origin), self.pixels_per_tile)
        if self.inverse_h:
            x = self.dimension[0] - x
        if self.inverse_v:
            y = self.dimension[1] - y
        return Point(x, y)

    def scale(self, vector: Vector2) -> Vector2:
        relative = v_mul(vector, self.pixels_per_tile)
        x, y = relative
        if self.inverse_h:
            x = - x
        if self.inverse_v:
            y = - y
        return Vector2(x, y)

    def view_origin(self, view_offset: Vector2=Vector2(0, 0)) -> Point:
        return Point(*v_add(self.anchor, view_offset))

    def view_dimension(self) -> Vector2:
        return Vector2(*v_div(self.dimension, self.pixels_per_tile))

    def view_rectangle(self, view_offset: Vector2=(0, 0)) -> Rectangle:
        return Rectangle(Point(*v_add(self.anchor, view_offset)), Vector2(*self.view_dimension()))


def calculate_anchor(rel_anchor: Tuple[float, float], dimension: Tuple[int, int], ppt: int) -> Vector2:
    return Vector2(*v_mul(v_sub(rel_anchor, (1, 1)), v_div(dimension, ppt)))