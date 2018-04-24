from api.scene import SceneContent
from api.utilities.geometry import Point
from api.graphics import get_cameras
from api.graphics.component import AutoGraphicsComponent, graphics_for
from api.graphics.camera import Camera
from api.graphics.drawing import f_default, C_BLACK, C_RED, C_YELLOW, C_GREEN, C_BLUE


class CameraMarker(SceneContent):
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
        txt = "'{}', {}".format(camera.cam_id, camera)
        self.font.render_to(surf=camera.render_target,
                            dest=self.target.offset_row1,
                            size=self.target.size,
                            fgcolor=self.target.colors[i],
                            bgcolor=C_BLACK,
                            text=txt)

        if camera.scene:
            txt = "@ '{}', {}".format(camera.scene.name, camera.scene)
        self.font.render_to(surf=camera.render_target,
                            dest=self.target.offset_row2, size=self.target.size,
                            fgcolor=self.target.colors[i],
                            bgcolor=C_BLACK,
                            text=txt)
