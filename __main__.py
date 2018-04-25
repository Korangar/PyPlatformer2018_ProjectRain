import api.graphics as graphics_system
import api.physics as physics_system
import api.scene as scene_system
from api.events import yield_api_events
from api.measurement.time import time_ms

updates_per_sec = 30
update_delay = 1000/updates_per_sec
delta_time = 0
avg_redraw_rate = 0.0
avg_update_delay = 0.0


if __name__ == "__main__":
    # init
    graphics_system.init_display(full_screen=True)
    start_scene = scene_system.SceneObject()
    from api.prefab.debug.camera_marker import CameraMarker
    scene_system.add_content_to_scene(start_scene, CameraMarker())
    from api.prefab.debug.fps_overlay import FpsOverlay
    scene_system.add_content_to_scene(start_scene, FpsOverlay())
    from api.prefab.background.plain_background import PlainBackground
    scene_system.add_content_to_scene(start_scene, PlainBackground())

    cam_anchor = scene_system.SceneContent()
    scene_system.add_content_to_scene(start_scene, cam_anchor)

    from api.prefab.ui.text import Text
    text = Text()
    scene_system.add_content_to_scene(start_scene, text)

    scene_system.change_active_scene(start_scene)
    from api.utilities.geometry import Point
    for target in graphics_system.get_camera_setup(0):
        c = graphics_system.Camera(Point(0, 0), "Main Camera", target)
        scene_system.add_content_to_scene(start_scene, c)

    # game loop
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
