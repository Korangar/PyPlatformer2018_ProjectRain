from api.sax_engine.core import ContentEntity
from api.sax_engine.core.systems.graphics import AutoGraphicsComponent, Camera
from api.sax_engine.core.systems.graphics.component import graphics_for
from api.sax_engine.core.systems.graphics.drawing import f_default
from api.sax_engine.geometry import Point

__all__ = ['TextContent']


class TextContent(ContentEntity):
    def __init__(self, position: Point, text: str="Hello World!") -> None:
        super().__init__(position)
        self.text = text
        self.f_color = (255, 255, 255)
        self.b_color = None
        self.size = 20


@graphics_for(TextContent)
class TextGraphics(AutoGraphicsComponent):
    def __init__(self, target: TextContent):
        super().__init__(target)
        self.font = f_default(self.target.size)

    def draw(self, camera: Camera) -> None:
        if camera.in_view(self.target.position):
            screen_pos = camera.project(self.target.position)
            self.font.render_to(camera.render_target, screen_pos, self.target.text,
                                fgcolor=self.target.f_color,
                                bgcolor=self.target.b_color)
