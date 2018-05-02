from .assertion import assert_on_init
from .tile_grid import Tile, Grid
from .vector import *

from typing import *


class Point(NamedTuple):
    x: float
    y: float

    def to_int(self)->Tuple[int, int]:
        return int(self.x), int(self.y)

    def on_grid(self, grid:Grid[Tile]):
        return 0 <= self.x <= len(grid) and 0 <= self.y <= len(grid[0])

    def get_tile(self, grid: Grid[Tile]) -> Tile:
        x, y = self.to_int()
        return grid[x][y]


@assert_on_init(lambda self: self.rad >= 0, "Radius can not be negative.")
class Circle(NamedTuple):
    pos: Point
    rad: float

    def get_tiles(self, grid: Grid[Tile]) -> Iterator[Tile]:
        raise Exception("Not yet implemented!")  # todo


@assert_on_init(lambda self: self.len >= 0, "Ray Length can not be negative.")
class Ray(NamedTuple):
    pos: Point
    end: Point
    dir: Vector2
    len: float

    def get_tiles(self, grid: Grid[Tile]) -> Generator[Tuple[Tile, Point, float], None, None]:
        point = self.pos
        for l in range(int(self.len)):
            if point.on_grid(grid):
                yield point.get_tile(grid), point, l
                point = Point(*v_add(self.pos, self.dir))
            else:
                break
        yield self.end.get_tile(grid), self.end, self.len


class Rectangle(NamedTuple):
    pos: Point
    dim: Vector2

    def max(self) -> Point:
        return Point(*v_max(self.pos, v_add(self.pos, self.dim)))

    def min(self) -> Point:
        return Point(*v_min(self.pos, v_add(self.pos, self.dim)))

    def intersect(self, other) -> bool:
        return intersect(self, other)

    def get_tiles(self, grid: Grid[Tile]) -> Iterator[Tile]:
        _min = v_max(self.min(), (0, 0))
        _max = v_min(self.max(), (len(grid), len(grid[0])))
        return (elm for row in zip(*grid[_min[0]:_max[0]])[_min[1]:_max[1]] for elm in row)

    def directional_projection(self, vector: Vector2, length: float=1) -> Tuple[Sequence[Ray], Sequence[Ray]]:
        h_dir, v_dir = vector
        if h_dir == 0:
            horizontal = tuple()
        else:
            if h_dir < 0:
                side = self.min().x
                _dir = Vector2(-1, 0)
            else:
                side = self.max().x
                _dir = Vector2(+1, 0)
            horizontal = tuple(
                create_ray(Point(side, self.pos.y + offset), _dir, length)
                for offset in inclusive_range(self.dim.y)
            )
        if v_dir == 0:
            vertical = tuple()
        else:
            if v_dir < 0:
                side = self.min().y
                _dir = Vector2(0, -1)
            else:
                side = self.max().y
                _dir = Vector2(0, +1)
            vertical = tuple(
                create_ray(Point(self.pos.x + offset, side), _dir, length)
                for offset in inclusive_range(self.dim.x)
            )
        return horizontal, vertical


# Union-type for all shapes
Shape = Union[Point, Circle, Ray, Rectangle]


# creation helper for rays
def create_ray(pos: Point, vec: Vector2, length: float=None) -> "Ray":
    if length is None:
        end: Point = Point(*vec)
        delta: Vector = v_sub(end, pos)
        normal: Vector2 = Vector2(*v_norm(delta))
        length: float = v_len(delta)
    else:
        end: Point = Point(*v_add(pos, v_mul(vec, length)))
        normal: Vector2 = vec
    return Ray(pos, end, normal, length)


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


def inclusive_range(delta: float):
    yield from range(int(delta))
    yield delta