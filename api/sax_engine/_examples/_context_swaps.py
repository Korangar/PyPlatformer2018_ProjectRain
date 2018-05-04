if __name__ == "__main__":
    import api.sax_engine.core as scene
    import api.sax_engine.core.systems.graphics as graphics
    from api.sax_engine.geometry import Point
    from api.sax_engine.events import yield_api_events

    from .example_content import *

    from time import sleep

    # create a screen and some render targets for the cameras
    graphics.init_display(full_screen=True)
    render_target = next(graphics.get_camera_setup(n_split=0))

    # create scenes
    scene0: scene.SceneObject = scene.SceneObject()
    scene1: scene.SceneObject = scene.SceneObject()

    # create content
    test_content0 = ExampleContentEntity(position=Point(0, 0))
    test_content1 = ExampleContentEntity(position=Point(1, 1))

    # add a camera to scene0
    from api.sax_engine.core.systems.graphics.camera import Camera
    scene.add_content_to_scene(scene0, Camera(Point(0, 0), "Main camera", render_target))

    # add a background clear to scene1
    from prefabs.background import PlainBackground
    scene.add_content_to_scene(scene1, PlainBackground((0, 0, 0)))

    # add camera markers to both scenes
    from prefabs.debug import CameraMarker
    scene.add_content_to_scene(scene0, CameraMarker())
    scene.add_content_to_scene(scene1, CameraMarker())

    # activate scene0
    scene.change_active_scene(scene0)
    graphics.update()
    sleep(1)
    yield_api_events()

    # add contents to scenes
    scene.add_content_to_scene(scene0, test_content0)
    scene.add_content_to_scene(scene1, test_content1)
    graphics.update()
    sleep(1)
    yield_api_events()

    # move content0 in scene0
    translation = Vector2(*v_mul(Vector2(-1, 1), 0.1))
    for i in range(100):
        test_content0.position = Point(*v_add(test_content0.position, translation))
        graphics.update()
        sleep(0.1)
        yield_api_events()

    # cache graphical context of scene0 and swap to scene1
    # core 1 does not have a background so the surface will not be cleared
    graphics.cache_active_context()
    scene.change_active_scene(scene1)
    graphics.update()
    sleep(1)
    yield_api_events()

    # add a camera to scene1
    scene.add_content_to_scene(scene1, Camera(Point(0, 0), "Main camera", render_target))
    graphics.update()
    sleep(1)
    yield_api_events()

    # move content1 in scene1
    test_content1.position = Point(*v_add(test_content1.position, Vector2(-1, -1)))
    graphics.update()
    sleep(1)
    yield_api_events()

    # swap to scene0 without caching
    scene.change_active_scene(scene0)
    graphics.update()
    sleep(1)
    yield_api_events()

    # swap back to scene1
    scene.change_active_scene(scene1)
    graphics.update()
    sleep(1)
    yield_api_events()
