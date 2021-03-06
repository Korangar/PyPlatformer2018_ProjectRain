from api.sax_engine.vector import *
from api.sax_engine.tile_grid import Tile, Grid

from .point import *
from .ray import *
from .circle import *
from .rectangle import *

__all__ = ['intersect', 'Shape', 'register_shape_on_grid', 'remove_shape_from_grid']


# Union-type for all shapes
Shape = Union[Point, Circle, Ray, Rectangle]


# basic intersect test
def intersect(shape1: Rectangle, shape2: Shape) -> bool:
    if isinstance(shape2, Point):
        shape2: Point
        max_s = shape1.max()
        min_s = shape1.min()
        return \
            min_s.x <= shape2.x <= max_s.x and \
            min_s.y <= shape2.y <= max_s.y
    elif isinstance(shape2, Circle):
        shape2: Circle
        if intersect(shape1, shape2.pos):
            return True
        else:
            test_point = v_min(shape1.max(), v_max(shape2.pos, shape1.min()))
            return v_lenq(v_sub(test_point, shape2.pos)) <= shape2.rad * shape2.rad
    elif isinstance(shape2, Ray):
        shape2: Ray
        tmin = 0.0
        tmax = shape2.len
        d1 = Vector2(*v_sub(shape1.pos, shape2.pos))
        d2 = Vector2(*v_add(d1, shape1.dim))
        if shape2.dir.x:
            tx = sorted(v_mul((d1.x, d2.x), 1 / shape2.dir.x))
            tmin = max(tmin, tx[0])
            tmax = min(tmax, tx[1])
        if shape2.dir.y:
            ty = sorted(v_mul((d1.y, d2.y), 1 / shape2.dir.y))
            tmin = max(tmin, ty[0])
            tmax = min(tmax, ty[1])
        return tmin <= tmax
    elif isinstance(shape2, Rectangle):
        rect: Rectangle = shape2
        max_s = shape1.max()
        min_s = shape1.min()
        max_r = rect.max()
        min_r = rect.min()
        return \
            min_s.x <= max_r.x and \
            min_r.x <= max_s.x and \
            min_s.y <= max_r.y and \
            min_r.y <= max_s.y
    else:
        return False


def register_shape_on_grid(grid: Grid[Tile], shape: Shape, value: Any=None):
    # todo remove the duck!
    for tile in shape.get_tiles(grid):
        if isinstance(tile, Sequence):
            tile = tile[0]
        tile.colliders.add(value if value else shape)


def remove_shape_from_grid(grid: Grid[Tile], shape: Shape, value: Any=None):
    for tile in shape.get_tiles(grid):
        if isinstance(tile, Sequence):
            tile = tile[0]
        if shape in tile.colliders:
            tile.colliders.remove(value if value else shape)
