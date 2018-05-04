from api.sax_engine.core import ContentEntity
from api.sax_engine.geometry import Point
from api.sax_engine.core.systems.graphics import get_cameras
from api.sax_engine.core.systems.graphics.component import AutoGraphicsComponent, graphics_for
from api.sax_engine.core.systems.graphics.camera import Camera
from api.sax_engine.core.systems.graphics.drawing import f_default, C_BLACK, C_RED, C_YELLOW, C_GREEN, C_BLUE

__all__ = ['CameraMarker']


class CameraMarker(ContentEntity):
    def __init__(self) -> None:
        super().__init__(Point(0, 0))
        self.size = 16
        self.offset_row1 = (5, -(5+self.size)*2)
        self.offset_row2 = (5, -(5+self.size))
        self.colors = [C_RED, C_YELLOW, C_GREEN, C_BLUE]


@graphics_for(CameraMarker)
class CameraMarkerGraphics(AutoGraphicsComponent):
    def __init__(self, target: CameraMarker):
        super().__init__(target)
        from math import inf
        self.sorting = inf
        self.font = f_default(self.target.size)

    def draw(self, camera: Camera) -> None:
        # TODO Draw this as an overlay

        i = get_cameras().index(camera)
        txt = "camera:'{}' in core:'{}' @ {}".format(camera.cam_id, camera.scene.name, camera.position)
        self.font.render_to(surf=camera.render_target,
                            dest=camera.screen_point(self.target.offset_row2),
                            fgcolor=self.target.colors[i],
                            bgcolor=C_BLACK,
                            text=txt)
