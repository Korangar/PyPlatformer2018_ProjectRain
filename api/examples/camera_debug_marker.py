from api.scene import SceneContent
from api.utilities.geometry import Point
from api.utilities.vector import *
from api.graphics import GraphicsInstruction, Camera, graphics_instruction
from api.graphics import f_default, RGB, get_cameras, C_BLACK, C_RED, C_YELLOW, C_GREEN, C_BLUE

from api.graphics import get_rate as fps_rate
from api.physics import get_rate as ups_rate


class CameraDebugMarker(SceneContent):
    def __init__(self) -> None:
        super().__init__(Point(0, 0))
        self.size = 16
        self.offset_row1 = (5, -(5+self.size)*2)
        self.offset_row2 = (5, -(5+self.size))
        self.colors = [C_RED, C_YELLOW, C_GREEN, C_BLUE]


@graphics_instruction(CameraDebugMarker)
class FpsOverlayGraphics(GraphicsInstruction[CameraDebugMarker]):
    def __init__(self, target: CameraDebugMarker):
        super().__init__(target)
        from math import inf
        self.sorting = inf
        self.font = f_default(self.target.size)

    def draw(self, camera: Camera) -> None:
        # TODO Draw this as an overlay

        i = get_cameras().index(camera)
        point = camera.get_screen_point(*self.target.offset_row1)
        txt = "'{}', {}".format(camera.cam_id, camera)
        self.font.render_to(surf=camera.target,
                            dest=point, size=self.target.size,
                            fgcolor=self.target.colors[i],
                            bgcolor=C_BLACK,
                            text=txt)

        point = camera.get_screen_point(*self.target.offset_row2)
        if camera.anchor.scene:
            txt = "@ '{}', {}".format(camera.anchor.scene.name, camera.anchor.scene)
        else:
            txt = "@ ''"
        self.font.render_to(surf=camera.target,
                            dest=point, size=self.target.size,
                            fgcolor=self.target.colors[i],
                            bgcolor=C_BLACK,
                            text=txt)
