from api.sax_engine.tile_grid import Tile, Grid, grid_size

from typing import *

__all__ = ['Point']


class Point(NamedTuple):
    x: float
    y: float

    def to_int(self) -> Tuple[int, int]:
        return int(self.x), int(self.y)

    def on_grid(self, grid: Grid[Tile]) -> bool:
        size = grid_size(grid)
        return (0 <= self.x < size.x and
                0 <= self.y < size.y)

    def get_tiles(self, grid: Grid[Tile]) -> Iterator[Tile]:
        x, y = self.to_int()
        return iter([grid[x][y]])
