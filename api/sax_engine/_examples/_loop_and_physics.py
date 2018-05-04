
if __name__ == "__main__":
    import api.sax_engine.core.systems.graphics as graphics_system
    import api.sax_engine.core.systems.physics as physics_system
    import api.sax_engine.core as scene_system
    from api.sax_engine.events import yield_api_events
    from api.sax_engine.timing.time import time_ms
    from api.sax_engine.geometry import Point
    from api.sax_engine.tile_grid import grid_size
    from api.sax_engine.vector import *

    updates_per_sec = 60
    update_delay = 1000 / updates_per_sec
    delta_time = 0
    avg_redraw_rate = 0.0
    avg_update_delay = 0.0

    graphics_system.init_display(full_screen=True)

    from .example_tile_grid import tile_map
    scene0 = scene_system.SceneObject(name="scene0", tile_grid=tile_map)

    from prefabs.debug import FpsOverlay
    scene_system.add_content_to_scene(scene0, FpsOverlay(Vector2(5, 5), (255, 0, 0)))

    from prefabs.debug import CameraMarker
    scene_system.add_content_to_scene(scene0, CameraMarker())

    from prefabs.background import TileGridRenderer
    tgr = TileGridRenderer()
    scene_system.add_content_to_scene(scene0, tgr)
    map_mid = v_mul(grid_size(tile_map), (0.5, 0.5))

    from .example_content import ExampleContentEntity
    content0 = ExampleContentEntity(position=Point(*v_add(map_mid, (0, 0))))
    scene_system.add_content_to_scene(scene0, content0)

    from api.sax_engine.core.systems.graphics.camera import Camera
    camera0 = Camera(Point(*map_mid), "camera 0", next(graphics_system.get_camera_setup()),
                     pixels_per_tile=16,
                     follow_target=content0,
                     grid_locks_view=True)
    scene_system.add_content_to_scene(scene0, camera0)

    from prefabs.utilities import TextContent
    scene_system.add_content_to_scene(scene0, TextContent(Point(*map_mid), "Fun with physics!"))
    scene_system.add_content_to_scene(scene0, TextContent(Point(55, 0), "Rock bottom!"))

    scene_system.change_active_scene(scene0)

    last_update = time_ms()
    update_loops_max = 5
    update_loops = 0
    while True:
        # update timing parameters
        time_since_update = time_ms() - last_update
        delta_time = time_since_update / 1000

        # event pump for pygame
        yield_api_events()

        if time_since_update > update_delay and update_loops < update_loops_max:
            # timing
            last_update += update_delay
            update_loops += 1

            scene_system.set_delta_time(delta_time)
            # update physics
            physics_system.update()
            # update core
            scene_system.update()
        else:
            # timing
            update_loops = 0

            # update graphics
            graphics_system.update()
