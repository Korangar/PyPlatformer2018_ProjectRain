from api.sax_engine.vector import *
import api.sax_engine.core.systems.graphics as graphics_system
import api.sax_engine.core as scene_system
from api.sax_engine.geometry import Point
from api.sax_engine.tile_grid import grid_size


def initialize():
    # noinspection PyProtectedMember
    from api.sax_engine._examples.example_tile_grid import tile_map
    # tile_map = list(zip(*tile_map))
    # t_wall = Tile("Wall", {"color": C_L_GRAY})
    # t_air = Tile("Air", {})
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
    from game.actors.player.player import Player

    from game.actors.pre_alpha_tier.pre_alpha_tier import PreAlphaTier
    for _ in range(0, 20, 4):
        pos = Point(*v_add(map_mid, (_, 0)))
        tier = PreAlphaTier(position=pos)
        scene_system.add_content_to_scene(scene0, tier)

    from api.sax_engine.core.systems.graphics.camera import Camera
    render_targets = list(graphics_system.get_camera_setup(0))
    player0 = Player(position=Point(*v_add(map_mid, (0, 0))), n=0)
    scene_system.add_content_to_scene(scene0, player0)
    camera0 = Camera(Point(*map_mid), "camera 0", render_targets[0],
                     pixels_per_tile=32,
                     follow_target=player0,
                     grid_locks_view=True)
    scene_system.add_content_to_scene(scene0, camera0)
    # player1 = Player(position=Point(*v_add(map_mid, (0, 0))), n=1)
    # scene_system.add_content_to_scene(scene0, player1)
    # camera1 = Camera(Point(*map_mid), "camera 1", render_targets[1],
    #                  pixels_per_tile=32,
    #                  follow_target=player1,
    #                  grid_locks_view=True)
    # scene_system.add_content_to_scene(scene0, camera1)

    # from prefabs.utilities import TextContent

    # scene_system.add_content_to_scene(scene0, TextContent(Point(*map_mid), "Fun with physics!"))
    # scene_system.add_content_to_scene(scene0, TextContent(Point(55, 0), "Rock bottom!"))

    scene_system.change_active_scene(scene0)
