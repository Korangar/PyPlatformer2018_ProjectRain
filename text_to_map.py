from typing import *

from api.sax_engine.tile_grid import *
from api.sax_engine.core.entities import SceneObject


def get_map() -> Tuple[Grid[Tile], List[SceneObject]]:
    spawnees = []
    tilegrid = [[]]

    return