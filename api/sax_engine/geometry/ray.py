from api.sax_engine.utilities.assertion import assert_on_init
from api.sax_engine.tile_grid import Tile, Grid
from api.sax_engine.vector import *

from .point import Point

from typing import *

__all__ = ['Ray', 'StaticRayCastResult', 'create_ray', 'static_ray_cast', 'multi_ray_cast', 'get_ray_from_hit']


@assert_on_init(lambda self: self.len >= 0, "Ray Length can not be negative.")
class Ray(NamedTuple):
    pos: Point
    end: Point
    dir: Vector2
    len: float

    def get_tiles(self, grid: Grid[Tile]) -> Generator[Tuple[Tile, Point, float], None, None]:
        point = self.pos
        for l in range(int(self.len)):
            if point.on_grid(grid):
                yield next(point.get_tiles(grid)), point, l
                point = Point(*v_add(point, self.dir))
            else:
                return
        if self.end.on_grid(grid):
            yield next(self.end.get_tiles(grid)), self.end, self.len


def create_ray(pos: Point, vec: Vector2, length: float = None) -> Ray:
    if length is None:
        end: Point = Point(*vec)
        delta: Vector = v_sub(end, pos)
        normal: Vector2 = Vector2(*v_norm(delta))
        length: float = v_len(delta)
    else:
        end: Point = Point(*v_add(pos, v_mul(vec, length)))
        normal: Vector2 = vec
    return Ray(pos, end, normal, length)


class StaticRayCastResult(NamedTuple):
    ray: Ray
    tile: Optional[Tile]
    point: Point
    distance: float


def static_ray_cast(ray: Ray, tile_grid: Grid[Tile], blocked_tiles: Sequence[Tile], collision_buffer: Set=None):
    tile = 0
    buffer_collisions = collision_buffer is not None
    for tile, point, distance in ray.get_tiles(tile_grid):
        if buffer_collisions:
            collision_buffer.update(tile.colliders)
        if tile in blocked_tiles:
            return StaticRayCastResult(ray, tile, point, distance)
    return StaticRayCastResult(ray, next(ray.end.get_tiles(tile_grid), None), ray.end, ray.len)


def multi_ray_cast(tile_grid: Grid[Tile],
                   blocked_tiles: Sequence[Tile],
                   *rays: Ray,
                   only_hits: bool=True,
                   collision_buffer: Set=None) -> Iterator[StaticRayCastResult]:
    ray_casts = (static_ray_cast(r, tile_grid, blocked_tiles, collision_buffer) for r in rays)
    if only_hits:
        return (hit for hit in ray_casts if hit.tile in blocked_tiles)
    else:
        return ray_casts


# creation helper for rays
def get_ray_from_hit(hit: StaticRayCastResult):
    return Ray(hit.ray.pos, hit.point, hit.ray.dir, hit.distance)
