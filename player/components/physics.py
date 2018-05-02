from api.physics.component import AutoPhysicsComponent, physics_for
from ..player import Player


@physics_for(Player)
class PlayerPhysics(AutoPhysicsComponent[Player]):
    def __init__(self, target: Player):
        super().__init__(target)

    def update(self) -> None:
        super().update()
