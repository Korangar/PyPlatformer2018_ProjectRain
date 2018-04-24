from api.scene import SceneContent
from api.utilities.geometry import Point
from api.utilities.vector import *
from api.graphics.component import AutoGraphicsComponent, graphics_for
from api.graphics.drawing import f_default, RGB, C_BLACK, C_SOMETHING
from api.graphics.camera import Camera

from api.graphics import get_rate as fps_rate
from api.physics import get_rate as ups_rate


class FpsOverlay(SceneContent):
    def __init__(self, offset: Vector2=Vector2(5, 5), color: RGB=C_SOMETHING, size: int = 16) -> None:
        super().__init__(Point(0, 0))
        self.size = size
        self.offset = offset
        self.color = color


@graphics_for(FpsOverlay)
class FpsOverlayGraphics(AutoGraphicsComponent):
    def __init__(self, target: FpsOverlay):
        super().__init__(target)
        from math import inf
        self.sorting = inf
        self.font = f_default(self.target.size)

    def draw(self, camera: Camera) -> None:
        # TODO Draw this as an overlay
        self.font.render_to(surf=camera.render_target,
                            dest=self.target.offset,
                            fgcolor=self.target.color,
                            bgcolor=C_BLACK,
                            size=self.target.size,
                            text='fps: {:.2f} | ups: {:.2f}'.format(fps_rate(), ups_rate()))
