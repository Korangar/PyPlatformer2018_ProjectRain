from api.examples.example_content import *

if __name__ == "__main__":
    from api.graphics.drawing import C_L_GRAY
    import api.graphics.system as graphics
    import api.scene.system as scene
    from api.events import yield_api_events
    from time import sleep

    graphics.init_display(full_screen=True)

    half_screen = Vector2(*v_mul(graphics.get_display().resolution, Vector2(0.5, 1)))
    quad_screen = Vector2(*v_mul(graphics.get_display().resolution, Vector2(0.5, 0.5)))

    scene0: scene.SceneObject = scene.SceneObject()

    from api.prefab.background.tile_grid_renderer import *
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

    from api.prefab.debug.fps_overlay import FpsOverlay
    scene.add_content_to_scene(scene0, FpsOverlay(Vector2(5, 5), (255, 0, 0)))

    from api.prefab.debug.camera_marker import CameraMarker
    scene.add_content_to_scene(scene0, CameraMarker())

    map_mid = Point(*v_mul(bg_manager.size, (0.5, 0.5)))
    content0 = ExampleContent(position=Point(*v_add(map_mid, (0, 0))))
    content1 = ExampleContent(position=Point(*v_add(map_mid, (1, 1))))
    content2 = ExampleContent(position=Point(*v_add(map_mid, (1, 0))))
    content3 = ExampleContent(position=Point(*v_add(map_mid, (0, 1))))

    scene.change_active_scene(scene0)
    scene.add_content_to_scene(scene0, content0)
    scene.add_content_to_scene(scene0, content1)
    test_ppt = (32, 16)
    for n, r in enumerate(graphics.get_screen_setup(1)):
        c = Camera(map_mid, "camera {}".format(n), r, pixels_per_tile=test_ppt[n])
        scene.add_content_to_scene(scene0, c)

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

    for c in graphics.get_cameras():
        scene.remove_content_from_scene(c.scene, c)

    test_ppt = (64, 32, 16, 8)
    for n, r in enumerate(graphics.get_screen_setup(2)):
        c = Camera(map_mid, "camera {}".format(n), r, pixels_per_tile=test_ppt[n])
        scene.add_content_to_scene(scene0, c)

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
