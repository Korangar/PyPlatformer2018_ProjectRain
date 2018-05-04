from api.sax_engine.core import ContentEntity
from api.sax_engine.geometry import Point
from api.sax_engine.core.systems.graphics.component import AutoGraphicsComponent, graphics_for
from api.sax_engine.core.systems.graphics.drawing import RGB
from api.sax_engine.core.systems.graphics.camera import Camera

__all__ = ['PlainBackground']


class PlainBackground(ContentEntity):
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
