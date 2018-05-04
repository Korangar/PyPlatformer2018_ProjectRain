from api.sax_engine.geometry import Point, Rectangle, multi_ray_cast
from api.sax_engine.vector import *
from api.sax_engine.core.systems.physics.component import AutoPhysicsComponent, physics_for
from api.sax_engine.tile_grid import alignment_correction
from api.sax_engine._examples.example_tile_grid import t_wall

from ..pre_alpha_tier import PreAlphaTier
from ..event_id import EventId

blocked_tiles = [t_wall]


@physics_for(PreAlphaTier)
class PlayerPhysics(AutoPhysicsComponent[PreAlphaTier]):

    def update(self) -> None:
        g: Vector2 = Vector2(*v_mul((0, -1), self.target.physics_data.GRAVITY_MODIFIER))
        tile_grid = self.target.scene.tile_grid
        physics_data = self.target.physics_data
        delta_time = self.target.scene.delta_time
        bounding_box = Rectangle(self.target.position, physics_data.size)

        # calculate new velocity from acceleration
        physics_data.velocity = Vector2(*v_add(physics_data.velocity, v_mul(g, delta_time)))

        # calculate position change from velocity
        h_trans, v_trans = v_mul(physics_data.velocity, delta_time)

        # prepare static collision with bounding_box
        h_rays = bounding_box.directional_projection(h_trans, horizontal=True)
        # get all ray hits
        all_hits = (multi_ray_cast(tile_grid, blocked_tiles, *h_rays, only_hits=True))
        # try to select closest hit
        closest_hit = next(iter(sorted(all_hits, key=lambda h: h.distance)), None)
        # if there is any hit
        h_absorb = bool(closest_hit)
        if h_absorb:
            # correct horizontal translation and align it with tile
            correction = alignment_correction(closest_hit.point.x, closest_hit.ray.dir.x)
            h_trans = closest_hit.ray.dir.x * closest_hit.distance + correction

        v_rays = tuple(bounding_box.directional_projection(v_trans, horizontal=False))
        all_hits = tuple(multi_ray_cast(tile_grid, blocked_tiles, *v_rays, only_hits=True))
        closest_hit = next(iter(sorted(all_hits, key=lambda h: h.distance)), None)
        v_absorb = bool(closest_hit)
        if v_absorb:
            correction = alignment_correction(closest_hit.point.y, closest_hit.ray.dir.y)
            v_trans = closest_hit.ray.dir.y * closest_hit.distance + correction

        if v_trans < 0 and all_hits and (all_hits[0].ray != v_rays[0] or
                                         all_hits[-1].ray != v_rays[-1]):
            self.target.push_event(EventId.watch_out)

        # set new position
        self.target.position = Point(*v_add(self.target.position, (h_trans, v_trans)))

        # adjust velocity based on collision data
        h_vel, v_vel = physics_data.velocity
        if h_absorb:
            self.target.push_event(EventId.touch_wall, orientation=h_absorb)
            h_vel = 0
        if v_absorb:
            if v_vel < 0:
                self.target.push_event(EventId.touch_floor)
            else:
                self.target.push_event(EventId.touch_ceiling)
            v_vel = 0
        physics_data.velocity = Vector2(h_vel, v_vel)

