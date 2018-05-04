from api.sax_engine.vector import Vector2
from typing import *
import math

__all__ = ['Grid', 'Tile', 'grid_size', 'alignment_correction']


_GridType = TypeVar("_GridType")
Grid = (Sequence[Sequence[_GridType]])


class Tile:
    def __init__(self, tile_type: str, tile_info: Dict):
        self.tile_type = tile_type
        self.tile_info = tile_info
        self.colliders = set()

    def __repr__(self):
        return "{}, '{}'".format(type(self).__name__, self.tile_type)

    def __str__(self):
        return "'{}', {}".format(self.tile_type, self.tile_info)


def grid_size(grid: Grid) -> Vector2:
    return Vector2(len(grid), len(grid[0]))


def alignment_correction(position: float, direction: float) -> float:
    if direction > 0:
        return math.floor(position) - position
    elif direction < 0:
        return math.floor(position + 1) - position
    else:
        return 0.0
