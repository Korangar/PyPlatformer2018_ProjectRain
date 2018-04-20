from typing import *

from .content import SceneContent, Agent, Player
from ..utilities import Vector2


class SceneObject:

    name: str
    content: Set[SceneContent]
    agents: Set[Agent]
    players: Set[Player]
    tag_dictionary: Mapping[str, Set[SceneContent]]

    def __init__(self): ...

    def update(self, delta_time: float) -> None: ...