from api.sax_engine.core.systems.graphics.component import AutoGraphicsComponent, graphics_for, _Content
from api.sax_engine.core.systems.graphics.camera import Camera
from api.sax_engine.core.systems.graphics.drawing import *
from api.sax_engine.geometry import Rectangle, Point
from api.sax_engine.vector import *

from ..state_id import StateId
from ..player import Player


@graphics_for(Player)
class PlayerGraphics(AutoGraphicsComponent[Player]):
    def __init__(self, target: _Content):
        super().__init__(target)
        self.font = f_default(15)

    def draw(self, camera: Camera) -> None:
        if camera.in_view(self.target.position):
            px, py = position = camera.project(self.target.position)
            dx, dy = dimension = camera.projection.scale(self.target.physics_data.size)
            camera.render_target.fill(C_WHITE, (px, py+dy, dx, abs(dy)))
            r = Rectangle(self.target.position, self.target.physics_data.size)
            r_min = camera.project(r.min()).to_int()
            r_max = camera.project(r.max()).to_int()
            draw.line(camera.render_target, *r_min, *r_max, C_D_GRAY)

            # todo make an origin point for aiming or something
            o_xy = Vector2(*v_div(v_add(r_min, r_max), 2)).to_int()
            l_xy = camera.projection.scale(self.target.shared_data.look_direction).to_int()
            if self.target.state_machine.current_state.id == StateId.aiming:
                visor_radius = 4
                visor_length = 5
                visor_color = C_RED
            else:
                visor_radius = 2
                visor_length = 2
                visor_color = C_GREEN
            visor = v_add(o_xy, v_mul(l_xy, visor_length))
            draw.line(camera.render_target, *o_xy, *visor, visor_color)
            draw.circle(camera.render_target, *visor, visor_radius, visor_color)

        if camera.follow_target == self.target:
            cam_w, cam_h = camera.render_target.get_size()
            rows = range(0, cam_h, int(self.font.size + 5))
            text = (self.target.position,
                    self.target.state_machine.current_state.id.name)
            h_w = cam_w/2
            for row, text in zip(rows, text):
                self.font.render_to(camera.render_target,
                                    (h_w, row),
                                    str(text),
                                    C_L_GRAY,
                                    C_BLACK)
