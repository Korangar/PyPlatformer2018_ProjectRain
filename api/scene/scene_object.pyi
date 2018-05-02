from typing import *

from .content import SceneContent, Actor
from ..utilities.tile_grid import Tile, Grid


class SceneObject:

    name: str
    delta_time: float
    current_time: float

    tile_grid: Grid[Tile]

    tag_dictionary: Mapping[str, Set[SceneContent]]
    content: Set[SceneContent]
    actors: Set[Actor]

    def __init__(self, name:str='', tile_grid:Grid[Tile]=None): ...