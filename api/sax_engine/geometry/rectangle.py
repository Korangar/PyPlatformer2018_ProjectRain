from api.sax_engine.tile_grid import Tile, Grid, grid_size
from api.sax_engine.vector import *

from .point import *
from .ray import *

from typing import *

__all__ = ['Rectangle']


class Rectangle(NamedTuple):
    pos: Point
    dim: Vector2
    side_buffer: float = 0.01

    def max(self) -> Point:
        return Point(*v_max(self.pos, v_add(self.pos, self.dim)))

    def min(self) -> Point:
        return Point(*v_min(self.pos, v_add(self.pos, self.dim)))

    def intersect(self, other) -> bool:
        from .shape_collision import intersect
        return intersect(self, other)

    def get_tiles(self, grid: Grid[Tile]) -> Iterator[Tuple[Tile, Point]]:
        min_x, min_y = v_max(self.min().to_int(), (0, 0))
        max_x, max_y = v_min(v_add(self.max().to_int(), (1, 1)), grid_size(grid))
        grid_crop = tuple(zip(*grid[min_x: max_x]))[min_y:max_y]
        return ((elm, Point(min_x+x, min_y+y))
                for y, row in enumerate(grid_crop)
                for x, elm in enumerate(row))

    def directional_projection(self,
                               translation: float,
                               horizontal: bool=True) -> Iterator[Ray]:
        # shoot rays out of points aligned on one of the rectangles edges
        if translation == 0:
            return tuple()
        else:
            if translation < 0:
                translation = abs(translation)
                line = self.min()
                orientation = -1
            else:
                line = self.max()
                orientation = +1

            if horizontal:
                _dir = Vector2(orientation, 0)
                return (create_ray(Point(line.x, self.pos.y + offset), _dir, translation)
                        for offset in self.dimension_in_chunks(horizontal=False))
            else:
                _dir = Vector2(0, orientation)
                return (create_ray(Point(self.pos.x + offset, line.y), _dir, translation)
                        for offset in self.dimension_in_chunks(horizontal=True))

    def dimension_in_chunks(self, horizontal: bool=True):
        if horizontal:
            delta = self.dim.x
        else:
            delta = self.dim.y
        yield from (self.side_buffer, *range(1, int(delta)), delta - self.side_buffer)
