from api.examples._example_content import *


if __name__ == "__main__":
    import api.graphics.system as graphics
    import api.scene.system as scene
    from api.events import yield_api_events
    from time import sleep

    graphics.init_display(full_screen=True)

    half_screen = Vector2(*v_mul(graphics.get_display().resolution, Vector2(0.5, 1)))
    quad_screen = Vector2(*v_mul(graphics.get_display().resolution, Vector2(0.5, 0.5)))

    scene0: scene.SceneObject = scene.SceneObject()

    from api.examples.tile_grid_renderer import *
    t_wall = Tile("Wall", {"color": C_L_GRAY})
    t_air = Tile("Air", {})
    tile_map = [[t_wall] * 150] + \
               [[t_wall] + [t_air] * 148 + [t_wall]] * 50 + \
               [[t_wall] * 150] + \
               [[t_wall] + [t_air] * 148 + [t_wall]] * 48 + \
               [[t_wall] * 150] + \
               [[t_wall] + [t_air] * 148 + [t_wall]] * 50 + \
               [[t_wall] * 150]
    bg_manager = TileGridRenderer(tile_map, 32)
    scene.add_content_to_scene(scene0, bg_manager)

    from api.examples.fps_overlay import FpsOverlay
    scene.add_content_to_scene(scene0, FpsOverlay(Vector2(5, 5), (255, 0, 0)))

    from api.examples.camera_debug_marker import CameraDebugMarker
    scene.add_content_to_scene(scene0, CameraDebugMarker())

    map_mid = v_mul(bg_manager.size, (0.5, 0.5))
    content0 = ExampleContent(position=Point(*v_add(map_mid, (0, 0))))
    content1 = ExampleContent(position=Point(*v_add(map_mid, (1, 1))))
    content2 = ExampleContent(position=Point(*v_add(map_mid, (1, 0))))
    content3 = ExampleContent(position=Point(*v_add(map_mid, (0, 1))))

    scene.change_active_scene(scene0)
    scene.add_content_to_scene(scene0, content0)
    scene.add_content_to_scene(scene0, content1)
    graphics.add_camera(content0,
                        target_dim=half_screen,
                        pixels_per_tile=32,
                        source_rel_off=Vector2(-.5, -.5),
                        target_rel_off=Vector2(0, 0))
    graphics.add_camera(content1,
                        target_dim=half_screen,
                        pixels_per_tile=16,
                        source_rel_off=Vector2(-.5, -.5),
                        target_rel_off=Vector2(1, 0))

    seconds = 5
    delta_time = 1.0/60
    translation = Vector2(*v_mul(Vector2(-1, 0), delta_time))
    for i in range(int(seconds/delta_time)):
        content0.position = Point(*v_add(content0.position, translation))
        graphics.update()
        sleep(delta_time)
        yield_api_events()

    scene.add_content_to_scene(scene0, content2)
    scene.add_content_to_scene(scene0, content3)
    graphics.update()
    sleep(1)
    yield_api_events()

    graphics.clear_cameras()
    graphics.add_camera(content0,
                        target_dim=quad_screen,
                        pixels_per_tile=64,
                        source_rel_off=Vector2(-.5, -.5),
                        target_rel_off=Vector2(0, 0))
    graphics.add_camera(content1,
                        target_dim=quad_screen,
                        pixels_per_tile=32,
                        source_rel_off=Vector2(-.5, -.5),
                        target_rel_off=Vector2(1, 0))
    graphics.add_camera(content2,
                        target_dim=quad_screen,
                        pixels_per_tile=16,
                        source_rel_off=Vector2(-.5, -.5),
                        target_rel_off=Vector2(0, 1))
    graphics.add_camera(content3,
                        target_dim=quad_screen,
                        pixels_per_tile=8,
                        source_rel_off=Vector2(-.5, -.5),
                        target_rel_off=Vector2(1, 1))
    graphics.update()
    sleep(1)
    yield_api_events()

    seconds = 5
    delta_time = 1.0 / 30
    translation = Vector2(*v_mul(Vector2(1, 0), delta_time))
    for i in range(int(seconds / delta_time)):
        content0.position = Point(*v_add(content0.position, translation))
        graphics.update()
        sleep(delta_time)
        yield_api_events()

    sleep(1)
    yield_api_events()
