from api.examples.example_content import *

if __name__ == "__main__":
    import api.graphics.system as graphics
    import api.scene.system as scene
    from api.events import yield_api_events
    from time import sleep

    graphics.init_display(full_screen=True)

    from api.examples.example_tile_grid import tile_map
    scene0 = scene.SceneObject(name="scene0", tile_grid=tile_map)

    from api.prefab.debug.fps_overlay import FpsOverlay
    scene.add_content_to_scene(scene0, FpsOverlay(Vector2(5, 5), (255, 0, 0)))

    from api.prefab.debug.camera_marker import CameraMarker
    scene.add_content_to_scene(scene0, CameraMarker())

    from api.prefab.background.tile_grid_renderer import *
    tgr = TileGridRenderer()
    scene.add_content_to_scene(scene0, tgr)

    map_mid = Point(*v_mul(tgr.grid_size(), (0.5, 0.5)))
    content0 = ExampleContent(position=Point(*v_add(map_mid, (0, 0))))
    content1 = ExampleContent(position=Point(*v_add(map_mid, (1, 1))))
    content2 = ExampleContent(position=Point(*v_add(map_mid, (1, 0))))
    content3 = ExampleContent(position=Point(*v_add(map_mid, (0, 1))))

    scene.change_active_scene(scene0)
    scene.add_content_to_scene(scene0, content0)
    scene.add_content_to_scene(scene0, content1)
    test_ppt = (32, 16)
    for n, r in enumerate(graphics.get_camera_setup(1)):
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

    scene.remove_content_from_scene(graphics.get_active_scene(), *graphics.get_cameras())

    test_ppt = (64, 32, 16, 8)
    for n, r in enumerate(graphics.get_camera_setup(2)):
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
