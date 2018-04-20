from ..utilities.geometry import Point
from ..utilities.vector import *


class Camera:
    def __init__(self, cam_id, view, anchor, target, ppt):
        self.cam_id = cam_id
        self.view = view
        self.anchor = anchor
        self.target = target
        self.ppt = ppt

    def is_in_view(self, point):
        return self.view.inside_source(point, self.anchor.position)

    def is_on_screen(self, point):
        return self.view.inside_target(point)

    def get_view_origin(self):
        return v_add(self.view.source_off, self.anchor.position)

    def get_screen_point(self, x, y):
        offset = self.target.get_offset()
        dimension = self.target.get_size()
        if isinstance(x, int):
            x = offset[0] + (x + dimension[0]) % dimension[0]
        else:
            x = offset[0] + x * dimension[0]
        if isinstance(y, int):
            y = offset[1] + (y + dimension[1]) % dimension[1]
        else:
            y = offset[1] + y * dimension[1]
        return Point(x, y)

    def project(self, point):
        px, py = Vector2(*v_mul(point, self.ppt)).to_int()
        ax, ay = Vector2(*v_mul(self.anchor.position, self.ppt)).to_int()
        vx, vy = Vector2(*v_mul(self.view.source_off, self.ppt)).to_int()
        dx, dy = Vector2(*v_mul(self.view.source_dim, self.ppt)).to_int()
        # TODO This works great, move it somewhere appropriate
        return Point(px-ax-vx, dy-(py-ay-vy))
