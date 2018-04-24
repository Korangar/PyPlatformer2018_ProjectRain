from api.scene.system import SceneContent
from api.graphics.camera import Camera
from api.graphics.component import AutoGraphicsComponent, graphics_for
from api.graphics.drawing import gfxdraw, C_WHITE
from api.utilities.geometry import Point
from api.utilities.vector import *


class ExampleContent(SceneContent):
    def __init__(self, position: Point):
        SceneContent.__init__(self, position)


@graphics_for(ExampleContent)
class ExampleContentGraphics(AutoGraphicsComponent):
    def __init__(self, target: ExampleContent):
        AutoGraphicsComponent.__init__(self, target)
        self.sorting = 1

    def draw(self, camera: Camera) -> None:
        if camera.in_view(self.target.position):
            position = camera.project(self.target.position)
            v11 = Vector2(1, 1)
            dimension = camera.projection.scale(v11)
            gfxdraw.rectangle(camera.render_target, (position, dimension), C_WHITE)
