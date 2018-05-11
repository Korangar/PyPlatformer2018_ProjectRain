from api.sax_engine.core import ContentEntity, remove_content_from_scene
from api.sax_engine.core.systems.graphics.component import AutoGraphicsComponent, graphics_for
from api.sax_engine.core.systems.graphics.camera import Camera
from api.sax_engine.core.systems.graphics.drawing import *
from api.sax_engine.geometry import Ray


__all__ = ['LineMarker']


class LineMarker(ContentEntity):
    def __init__(self, ray: Ray, color: RGB, seconds: float = 0):
        super().__init__(ray.pos)
        self.ray_end = ray.end
        self.color = color
        self.seconds = seconds
        self.spawn_time = 0

    def is_alive(self):
        return self.seconds == 0 or self.get_scene_time()-self.spawn_time < self.seconds

    def spawn(self):
        self.spawn_time = self.get_scene_time()


@graphics_for(LineMarker)
class LineMarkerGraphics(AutoGraphicsComponent[LineMarker]):
    def __init__(self, target: LineMarker):
        super().__init__(target)
        from math import inf
        self.sorting = inf

    def draw(self, camera: Camera) -> None:
        if self.target.is_alive():
            pos = camera.project(self.target.position).to_int()
            end = camera.project(self.target.ray_end).to_int()
            draw.line(camera.render_target, *pos, *end, self.target.color)
        else:
            remove_content_from_scene(self.target.scene, self.target)
