from api.scene.system import SceneContent
from api.graphics import Camera, GraphicsInstruction, graphics_instruction
from api.graphics import gfxdraw, C_WHITE
from api.utilities.geometry import Point
from api.utilities.vector import *


class ExampleContent(SceneContent):
    def __init__(self, position: Point):
        SceneContent.__init__(self, position)


@graphics_instruction(ExampleContent)
class ExampleContentGraphics(GraphicsInstruction[ExampleContent]):
    def __init__(self, target: ExampleContent):
        GraphicsInstruction.__init__(self, target)
        self.sorting = 1

    def draw(self, camera: Camera) -> None:
        if camera.is_in_view(self.target.position):
            position = camera.project(self.target.position)
            v11 = Vector2(1, 1)
            dimension = camera.view.scale(v11)
            gfxdraw.rectangle(camera.target, (position, dimension), C_WHITE)
