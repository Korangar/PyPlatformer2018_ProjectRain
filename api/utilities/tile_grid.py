from api.utilities.geometry import *

from typing import *

_GridType = TypeVar("_GridType")
Grid = (Sequence[Sequence[_GridType]])


class Tile:
    def __init__(self, tile_type: str, tile_info: Dict):
        self.tile_type = tile_type
        self.tile_info = tile_info

    def __repr__(self):
        return "{}, '{}'".format(type(self).__name__, self.tile_type)

    def __str__(self):
        return "'{}', {}".format(self.tile_type, self.tile_info)


def scan_grid(grid: Grid, shape: Shape) -> Iterator[Tile]:
    if isinstance(shape, Point):
        point: Point = shape
        return tuple(grid[int(point.x)][int(point.y)])
    elif isinstance(shape, Circle):
        shape: Circle
        raise Exception("Not yet implemented!")
    elif isinstance(shape, Ray):
        shape: Ray
        raise Exception("Not yet implemented!")
    elif isinstance(shape, Rectangle):
        rect: Rectangle = shape
        _min = v_max(rect.min(), (0, 0))
        _max = v_min(rect.max(), (len(grid), len(grid[0])))
        return iter(elm for row in zip(*grid[_min[0]:_max[0]])[_min[1]:_max[1]] for elm in row)
    return ()
