from api.sax_engine.vector import *
import api.sax_engine.core.systems.graphics as graphics_system
import api.sax_engine.core as scene_system
from api.sax_engine.geometry import Point
from api.sax_engine.tile_grid import grid_size


def initialize():
    # noinspection PyProtectedMember
    from api.sax_engine._examples.example_tile_grid import tile_map
    scene0 = scene_system.SceneObject(name="scene0", tile_grid=tile_map)

    # import and create debug related stuff
    from prefabs.debug import FpsOverlay
    scene_system.add_content_to_scene(scene0, FpsOverlay(Vector2(5, 5), (255, 0, 0)))
    from prefabs.debug import CameraMarker
    scene_system.add_content_to_scene(scene0, CameraMarker())

    from prefabs.background import TileGridRenderer

    tgr = TileGridRenderer()
    scene_system.add_content_to_scene(scene0, tgr)
    map_mid = v_mul(grid_size(tile_map), (0.5, 0.5))

    # import and create player
    from player.player import Player
    player = Player(position=Point(*v_add(map_mid, (0, 0))))
    scene_system.add_content_to_scene(scene0, player)

    from pre_alpha_tier.pre_alpha_tier import PreAlphaTier
    tier = PreAlphaTier(position=Point(*v_add(map_mid, (0, 0))))
    scene_system.add_content_to_scene(scene0, tier)

    from api.sax_engine.core.systems.graphics.camera import Camera

    camera0 = Camera(Point(*map_mid), "camera 0", next(graphics_system.get_camera_setup()),
                     pixels_per_tile=32,
                     follow_target=player,
                     grid_locks_view=True)
    scene_system.add_content_to_scene(scene0, camera0)

    from prefabs.utilities import TextContent

    scene_system.add_content_to_scene(scene0, TextContent(Point(*map_mid), "Fun with physics!"))
    scene_system.add_content_to_scene(scene0, TextContent(Point(55, 0), "Rock bottom!"))

    scene_system.change_active_scene(scene0)
