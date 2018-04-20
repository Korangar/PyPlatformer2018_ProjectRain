from .geometry import Point, Rectangle
from .vector import *

from typing import *


class Projection(NamedTuple):
    source_off: Vector2
    source_dim: Vector2
    target_off: Vector2
    target_dim: Vector2
    inverse_h: float
    inverse_v: float

    def check_aspect_distortion(self) -> bool:
        a, b = v_div(self.source_dim, self.target_dim)
        return a == b

    def inverse(self) -> "Projection":
        return Projection(source_off=self.target_off,
                          source_dim=self.target_dim,
                          target_off=self.source_off,
                          target_dim=self.source_dim,
                          inverse_h=self.inverse_h,
                          inverse_v=self.inverse_v)

    def inside_source(self, point: Point, source_pos: Vector2=(0, 0)) -> bool:
        rect = Rectangle(v_add(self.source_off, source_pos), self.source_dim)
        return rect.intersect(point)

    def inside_target(self, point: Point, target_pos: Vector2=(0, 0)) -> bool:
        rect = Rectangle(v_add(self.target_off, target_pos), self.target_dim)
        return rect.intersect(point)

    def project(self, point: Point, source_pos: Point = Point(0, 0), target_pos: Point = Point(0, 0)) -> Point:
        source_origin = v_add(self.source_off, source_pos)
        target_origin = v_add(self.target_off, target_pos)
        x, y = v_div(v_sub(point, source_origin), self.source_dim)
        if self.inverse_h:
            x = 1 - x
        if self.inverse_v:
            y = 1 - y
        target_point = Point(*v_add(target_origin, v_mul((x, y), self.target_dim)))
        return target_point

    def scale(self, vector: Vector2) -> Vector2:
        relative = v_div(vector, self.source_dim)
        x, y = relative
        if self.inverse_h:
            x = - x
        if self.inverse_v:
            y = - y
        scaled = Vector2(*v_mul((x, y), self.target_dim))
        return scaled
