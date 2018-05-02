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
from api.utilities.tile_grid import Tile, alignment_correction
from .example_tile_grid import t_air, t_wall


class StaticRayHit(NamedTuple):
    ray: Ray
    tile: Tile
    point: Point
    distance: float

    def shorten_ray(self) -> Ray:
        return Ray(self.ray.pos, self.point, self.ray.dir, self.distance)


@physics_for(ExampleContent)
class ExampleContentPhysics(AutoPhysicsComponent[ExampleContent]):
    def __init__(self, target: ExampleContent):
        super().__init__(target)

    def update(self, delta_time: float, g: Vector2=Vector2(-1, -1)) -> None:
        self.target.contact_points.clear()
        bounding_box = Rectangle(self.target.position, self.target.size)

        self.velocity = Vector2(*v_add(self.velocity, v_mul(g, delta_time)))
        h_trans, v_trans = translation = v_mul(self.velocity, delta_time)
        h_rays, v_rays = bounding_box.directional_projection(v_norm(translation), v_len(translation))

        hits_sorted = list(sorted(filter(bool, map(self.static_ray_hit, h_rays)), key=lambda hit: hit.distance))
        h_absorb = bool(hits_sorted)
        if h_absorb:
            hit = hits_sorted[0]
            # select closest hit distance and correct it to align with tile
            h_trans = hit.ray.dir.x * hit.distance + alignment_correction(hit.point.x, hit.ray.dir.x)

        hits_sorted = list(sorted(filter(bool, map(self.static_ray_hit, v_rays)), key=lambda hit: hit.distance))
        v_absorb = bool(hits_sorted)
        if v_absorb:
            self.target.contact_points.extend((hit.ray.pos for hit in hits_sorted))
            hit = hits_sorted[0]
            v_trans = hit.ray.dir.y * hit.distance + alignment_correction(hit.point.y, hit.ray.dir.y)

        self.target.position = Point(*v_add(self.target.position, (h_trans, v_trans)))
        # todo observer for absorbing velocity
        h_vel, v_vel = self.velocity
        if h_absorb:
            h_vel = -h_vel
        if v_absorb:
            v_vel = -v_vel
        self.velocity = Vector2(h_vel, v_vel)

    def static_ray_hit(self, ray: Ray) -> StaticRayHit:
        for tile, point, distance in ray.get_tiles(self.target.scene.tile_grid):
            if tile == t_wall:
                return StaticRayHit(ray, tile, point, distance)
