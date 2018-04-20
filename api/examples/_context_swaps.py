from api.examples._example_content import *
from api.examples.tile_grid_renderer import *


if __name__ == "__main__":
    import api.graphics.system as graphics
    import api.scene.system as scene
    from api.events import yield_api_events
    from time import sleep

    test_scene0: scene.SceneObject = scene.SceneObject()
    test_content0 = ExampleContent(position=Point(0, 0))
    test_scene1: scene.SceneObject = scene.SceneObject()
    test_content1 = ExampleContent(position=Point(1, 1))

    from api.examples.background_cleaner import BackgroundCleaner
    scene.add_content_to_scene(test_scene1, BackgroundCleaner((0, 0, 0)))

    from api.examples.camera_debug_marker import CameraDebugMarker
    scene.add_content_to_scene(test_scene0, CameraDebugMarker())
    scene.add_content_to_scene(test_scene1, CameraDebugMarker())

    graphics.init_display(full_screen=True)

    scene.change_active_scene(test_scene0)
    graphics.add_camera(test_content0,
                        target_dim=Vector2(*graphics.get_display().resolution),
                        pixels_per_tile=64,
                        source_rel_off=Vector2(-.5, -.5))
    graphics.update()
    sleep(1)
    yield_api_events()

    scene.add_content_to_scene(test_scene0, test_content0)
    scene.add_content_to_scene(test_scene1, test_content1)
    graphics.update()
    sleep(1)
    yield_api_events()

    translation = Vector2(*v_mul(Vector2(-1, 1), 0.1))
    for i in range(100):
        test_content0.position = Point(*v_add(test_content0.position, translation))
        graphics.update()
        sleep(0.1)
        yield_api_events()

    graphics.cache_active_context()
    scene.change_active_scene(test_scene1)
    graphics.update()
    sleep(1)
    yield_api_events()

    graphics.add_camera(test_content0,
                        target_dim=Vector2(*graphics.get_display().resolution),
                        pixels_per_tile=32,
                        source_rel_off=Vector2(-.5, -.5))
    graphics.update()
    sleep(1)
    yield_api_events()

    test_content1.position = Point(*v_add(test_content1.position, Vector2(-1, -1)))
    graphics.update()
    sleep(1)
    yield_api_events()

    scene.change_active_scene(test_scene0)
    graphics.update()
    sleep(1)
    yield_api_events()

    scene.change_active_scene(test_scene1)
    graphics.update()
    sleep(1)
    yield_api_events()
