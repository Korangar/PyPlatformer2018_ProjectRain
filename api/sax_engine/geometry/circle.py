from api.sax_engine.utilities.assertion import assert_on_init
from api.sax_engine.tile_grid import Tile, Grid

from .point import Point

from typing import *

__all__ = ['Circle']


@assert_on_init(lambda self: self.rad >= 0, "Radius can not be negative.")
class Circle(NamedTuple):
    pos: Point
    rad: float

    def get_tiles(self, grid: Grid[Tile]) -> Iterator[Tile]:
        raise Exception("Not yet implemented!")  # todo