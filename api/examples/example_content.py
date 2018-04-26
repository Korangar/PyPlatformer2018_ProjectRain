from api.scene.system import SceneContent
from api.utilities.geometry import Point, Ray
from api.utilities.vector import *


class ExampleContent(SceneContent):
    def __init__(self, position: Point):
        SceneContent.__init__(self, position)
        self.size = Vector2(1, 1)
        self.contact_points = []


from api.graphics.camera import Camera
from api.graphics.component import AutoGraphicsComponent, graphics_for
from api.graphics.drawing import gfxdraw, C_WHITE, C_RED


@graphics_for(ExampleContent)
class ExampleContentGraphics(AutoGraphicsComponent[ExampleContent]):
    def __init__(self, target: ExampleContent):
        AutoGraphicsComponent.__init__(self, target)
        self.sorting = 1

    def draw(self, camera: Camera) -> None:
        if camera.in_view(self.target.position):
            position = camera.project(self.target.position)
            dimension = camera.projection.scale(self.target.size)
            gfxdraw.rectangle(camera.render_target, (position, dimension), C_WHITE)
            if self.target.contact_points:
                p1, p2 = self.target.contact_points
                gfxdraw.line(camera.render_target, *camera.project(p1).to_int(), *camera.project(p2).to_int(), C_RED)

            r = Rectangle(self.target.position, self.target.size)
            gfxdraw.line(camera.render_target, *camera.project(r.min()).to_int(), *camera.project(r.max()).to_int(), C_RED)
            gfxdraw.circle(camera.render_target, *camera.project(r.min()).to_int(), 3, C_WHITE)


from api.physics.component import AutoPhysicsComponent, physics_for
from api.utilities.geometry import Rectangle
from .example_tile_grid import Tile, t_air, t_wall


@physics_for(ExampleContent)
class ExampleContentPhysics(AutoPhysicsComponent[ExampleContent]):
    def __init__(self, target: ExampleContent):
        super().__init__(target)

    def update(self, delta_time: float, g: Vector2=Vector2(0, -1)) -> None:
        self.target.contact_points.clear()
        bounding_box = Rectangle(self.target.position, self.target.size)

        self.velocity = Vector2(*v_add(self.velocity, v_mul(g, delta_time)))
        h_trans, v_trans = translation = v_mul(self.velocity, delta_time)
        h_rays, v_rays = bounding_box.directional_projection(v_norm(translation), v_len(translation))

        hit_sort = list(filter(bool, map(self.static_ray_hit, h_rays)))
        h_absorb = bool(hit_sort)
        if h_absorb:
            hit_sort.sort(key=lambda tl: tl[1])
            r, t, h_trans = hit_sort[0]

        hit_sort = list(filter(bool, map(self.static_ray_hit, v_rays)))
        v_absorb = bool(hit_sort)
        if v_absorb:
            hit_sort.sort(key=lambda rtl: rtl[-1])
            self.target.contact_points.extend((r.pos for r, t, l in hit_sort))
            r, t, v_trans = hit_sort[0]

        self.target.position = Point(*v_add(Vector2(h_trans, v_trans), self.target.position))
        # todo observer for absorbing velocity
        h_vel, v_vel = self.velocity
        if h_absorb:
            h_vel = 0
        if v_absorb:
            v_vel = 0
        self.velocity = Vector2(h_vel, v_vel)


    def static_ray_hit(self, ray: Ray) -> Tuple[Ray, Tile, float]:
        for tl in ray.on_grid(self.target.scene.tile_grid):
            if tl[0] == t_wall:
                return ray, tl[0], tl[1]
