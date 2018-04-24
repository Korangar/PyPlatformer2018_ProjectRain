from api.utilities.geometry import Point
from api.graphics.component import *
from api.graphics.drawing import *
from api.graphics.camera import *
from api.scene.content import *


class Text(SceneContent):
    def __init__(self, position: Point = (0, 0)) -> None:
        super().__init__(position)
        self.text = "Hello World!"
        self.f_color = (255, 255, 255)
        self.b_color = None
        self.size = 20


@graphics_for(Text)
class TextGraphics(AutoGraphicsComponent):
    def __init__(self, target: Text):
        super().__init__(target)
        self.font = f_default(self.target.size)

    def draw(self, camera: Camera) -> None:
        screen_pos = camera.project(self.target.position)
        self.font.render_to(camera.render_target, screen_pos, self.target.text,
                            fgcolor=self.target.f_color,
                            bgcolor=self.target.b_color)
