from api.scene import SceneContent
from api.utilities.geometry import Point
from api.graphics.component import AutoGraphicsComponent, graphics_for
from api.graphics.drawing import RGB
from api.graphics.camera import Camera


class PlainBackground(SceneContent):
    def __init__(self, color: RGB = (0, 0, 0)) -> None:
        super().__init__(Point(0, 0))
        self.color = color


@graphics_for(PlainBackground)
class PlainBackgroundGraphics(AutoGraphicsComponent):
    def __init__(self, target: PlainBackground):
        super().__init__(target)
        from math import inf
        self.sorting = -inf

    def draw(self, camera: Camera) -> None:
        camera.render_target.fill(self.target.color)
