from typing import *

from .content import SceneContent, Agent, Player
from ..utilities import Vector2
from ..utilities.tile_grid import Tile, Grid


class SceneObject:

    name: str
    tile_grid: Grid[Tile]
    content: Set[SceneContent]
    agents: Set[Agent]
    players: Set[Player]
    tag_dictionary: Mapping[str, Set[SceneContent]]

    def __init__(self, name:str='', tile_grid:Grid[Tile]=None): ...

    def update(self, delta_time: float) -> None: ...