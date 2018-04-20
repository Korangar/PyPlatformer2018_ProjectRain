from api.scene import SceneContent
from api.utilities.geometry import Point
from api.graphics import GraphicsInstruction, Camera, graphics_instruction
from api.graphics import RGB


class BackgroundCleaner(SceneContent):
    def __init__(self, color: RGB) -> None:
        super().__init__(Point(0, 0))
        self.color = color


@graphics_instruction(BackgroundCleaner)
class FpsOverlayGraphics(GraphicsInstruction[BackgroundCleaner]):
    def __init__(self, target: BackgroundCleaner):
        super().__init__(target)
        from math import inf
        self.sorting = -inf

    def draw(self, camera: Camera) -> None:
        camera.target.fill(self.target.color)
