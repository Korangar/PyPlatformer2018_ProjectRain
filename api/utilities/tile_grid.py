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
