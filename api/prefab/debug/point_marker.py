from api.scene import SceneContent, remove_content_from_scene
from api.graphics.component import AutoGraphicsComponent, graphics_for
from api.graphics.camera import Camera
from api.graphics.drawing import gfxdraw, RGB


class PointMarker(SceneContent):
    def __init__(self, position, color: RGB, seconds: float = 0):
        super().__init__(position)
        self.spawn_time = 0
        self.seconds = seconds
        self.color = color

    def is_alive(self):
        return self.seconds == 0 or self.get_scene_time()-self.spawn_time < self.seconds

    def spawn(self):
        self.spawn_time = self.get_scene_time()


@graphics_for(PointMarker)
class PointMarkerGraphics(AutoGraphicsComponent[PointMarker]):
    def __init__(self, target: PointMarker):
        super().__init__(target)
        from math import inf
        self.sorting = inf

    def draw(self, camera: Camera) -> None:
        if self.target.is_alive:
            position = camera.project(self.target.position)
            gfxdraw.rectangle(camera.render_target, (*position, 3, 3), self.target.color)
        else:
            # this might be unsafe
            remove_content_from_scene(self.target.scene, self.target)
