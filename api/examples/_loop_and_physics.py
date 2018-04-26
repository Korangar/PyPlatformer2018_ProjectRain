
if __name__ == "__main__":
    import api.graphics as graphics_system
    import api.physics as physics_system
    import api.scene as scene_system
    from api.events import yield_api_events
    from api.measurement.time import time_ms
    from api.utilities.geometry import Point
    from api.utilities.vector import *

    updates_per_sec = 30
    update_delay = 1000 / updates_per_sec
    delta_time = 0
    avg_redraw_rate = 0.0
    avg_update_delay = 0.0

    graphics_system.init_display(full_screen=True)

    from api.examples.example_tile_grid import tile_map
    scene0 = scene_system.SceneObject(name="scene0", tile_grid=tile_map)

    from api.prefab.debug.fps_overlay import FpsOverlay
    scene_system.add_content_to_scene(scene0, FpsOverlay(Vector2(5, 5), (255, 0, 0)))

    from api.prefab.debug.camera_marker import CameraMarker
    scene_system.add_content_to_scene(scene0, CameraMarker())

    from api.prefab.background.tile_grid_renderer import TileGridRenderer
    tgr = TileGridRenderer()
    scene_system.add_content_to_scene(scene0, tgr)
    map_mid = v_mul(tgr.grid_size(), (0.5, 0.5))

    from api.examples.example_content import ExampleContent
    content0 = ExampleContent(position=Point(*v_add(map_mid, (0, 0))))
    scene_system.add_content_to_scene(scene0, content0)

    from api.graphics.camera import Camera
    camera0 = Camera(Point(*map_mid), "camera 0", next(graphics_system.get_camera_setup()),
                     pixels_per_tile=16,
                     follow_target=None,
                     grid_locks_view=True)
    scene_system.add_content_to_scene(scene0, camera0)

    from api.prefab.ui.text import Text
    scene_system.add_content_to_scene(scene0, Text(Point(*map_mid), "Fun with physics!"))
    scene_system.add_content_to_scene(scene0, Text(Point(76, 0), "Rock bottom!"))

    scene_system.change_active_scene(scene0)

    last_update = time_ms()
    update_loops_max = 5
    update_loops = 0
    while True:
        # update measurement parameters
        time_since_update = time_ms() - last_update
        delta_time = time_since_update / 1000

        # event pump for pygame
        yield_api_events()

        if time_since_update > update_delay and update_loops < update_loops_max:
            # timing
            last_update += update_delay
            update_loops += 1

            # update physics
            physics_system.update(delta_time)
            # update scene
            scene_system.get_active_scene().update(delta_time)
        else:
            # timing
            update_loops = 0

            # update graphics
            graphics_system.update()