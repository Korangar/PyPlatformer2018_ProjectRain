from api.sax_engine.core import ContentEntity
from api.sax_engine.geometry import Point, Rectangle, Ray, StaticRayCastResult
from api.sax_engine.vector import *

from api.sax_engine.core.systems.graphics.component import AutoGraphicsComponent, graphics_for
from api.sax_engine.core.systems.graphics.drawing import draw, C_WHITE, C_RED
from api.sax_engine.core.systems.graphics.camera import Camera

from api.sax_engine.core.systems.physics.component import AutoPhysicsComponent, physics_for
from api.sax_engine.tile_grid import Tile, Grid, alignment_correction
from .example_tile_grid import t_wall


class ExampleContentEntity(ContentEntity):
    def __init__(self, position: Point):
        ContentEntity.__init__(self, position)
        self.size = Vector2(1, 1)
        self.contact_points = []


@graphics_for(ExampleContentEntity)
class ExampleContentGraphics(AutoGraphicsComponent[ExampleContentEntity]):
    def __init__(self, target: ExampleContentEntity):
        AutoGraphicsComponent.__init__(self, target)
        self.sorting = 1

    def draw(self, camera: Camera) -> None:
        if camera.in_view(self.target.position):
            position = camera.project(self.target.position)
            dimension = camera.projection.scale(self.target.size)
            draw.rectangle(camera.render_target, (position, dimension), C_WHITE)
            if self.target.contact_points:
                p1, p2 = self.target.contact_points
                draw.line(camera.render_target, *camera.project(p1).to_int(), *camera.project(p2).to_int(), C_RED)

            r = Rectangle(self.target.position, self.target.size)
            draw.line(camera.render_target,
                      *camera.project(r.min()).to_int(),
                      *camera.project(r.max()).to_int(), C_RED)
            draw.circle(camera.render_target,
                        *camera.project(r.min()).to_int(),
                        3,
                        C_WHITE)


@physics_for(ExampleContentEntity)
class ExampleContentPhysics(AutoPhysicsComponent[ExampleContentEntity]):
    def __init__(self, target: ExampleContentEntity):
        super().__init__(target)

    def update(self, g: Vector2 = Vector2(-1, -1)) -> None:
        self.target.contact_points.clear()
        bounding_box = Rectangle(self.target.position, self.target.size)

        self.velocity = Vector2(*v_add(self.velocity, v_mul(g, self.target.scene.delta_time)))
        h_trans, v_trans = translation = v_mul(self.velocity, self.target.scene.delta_time)
        h_rays, v_rays = bounding_box.directional_projection(v_norm(translation), v_len(translation))

        all_hits = static_ray_hits(self.target.scene.tile_grid, *h_rays)
        closest_hit = next(sorted(all_hits, key=lambda h: h.distance), default=None)
        h_absorb = bool(closest_hit)
        if h_absorb:
            # select closest hit distance and correct it to align with tile
            h_trans = closest_hit.ray.dir.x * closest_hit.distance + alignment_correction(closest_hit.point.x,
                                                                                          closest_hit.ray.dir.x)

        all_hits = static_ray_hits(self.target.scene.tile_grid, *v_rays)
        closest_hit = next(list(sorted(all_hits, key=lambda h: h.distance)), default=None)
        v_absorb = bool(closest_hit)
        if v_absorb:
            self.target.contact_points.extend((hit.ray.pos for hit in closest_hit))
            v_trans = closest_hit.ray.dir.y * closest_hit.distance + alignment_correction(closest_hit.point.y,
                                                                                          closest_hit.ray.dir.y)

        self.target.position = Point(*v_add(self.target.position, (h_trans, v_trans)))
        # todo observer for absorbing velocity
        h_vel, v_vel = self.velocity
        if h_absorb:
            h_vel = -h_vel
        if v_absorb:
            v_vel = -v_vel
        self.velocity = Vector2(h_vel, v_vel)


def static_ray_hits(tile_grid: Grid[Tile], *rays: Ray) -> Iterator[StaticRayCastResult]:
    ray_casts = (r.cast(tile_grid, t_wall) for r in rays)
    return (hit for hit in ray_casts if hit)
