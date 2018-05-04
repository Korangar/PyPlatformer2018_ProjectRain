from typing import *

from api.sax_engine.core.entities import ContentEntity, ActorEntity
from api.sax_engine.tile_grid import Tile, Grid


class SceneObject:

    name: str
    delta_time: float
    current_time: float

    tile_grid: Grid[Tile]

    tag_dictionary: Mapping[str, Set[ContentEntity]]
    content: Set[ContentEntity]
    actors: Set[ActorEntity]

    def __init__(self, name:str='', tile_grid:Grid[Tile]=None): ...