from api.graphics.component import AutoGraphicsComponent, graphics_for
from api.graphics.camera import Camera
from ..player import Player


@graphics_for(Player)
class PlayerGraphics(AutoGraphicsComponent[Player]):
    def __init__(self, target: Player):
        super().__init__(target)

    def draw(self, camera: Camera) -> None:
        super().draw(camera)
