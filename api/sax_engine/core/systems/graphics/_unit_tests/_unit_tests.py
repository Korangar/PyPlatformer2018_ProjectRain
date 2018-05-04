import api.sax_engine.core as core
from api.sax_engine.geometry import Point

from .. import _system as graphics
from ..component import graphics_for

import unittest


class TestContentEntity(core.ContentEntity):
    def __init__(self, position: Point) -> None:
        super().__init__(position)


@graphics_for(TestContentEntity)
class ExampleContentGraphics(graphics.AutoGraphicsComponent[TestContentEntity]):
    def draw(self, camera) -> None:
        pass


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.scene0 = core.SceneObject()
        self.scene1 = core.SceneObject()
        self.content0 = TestContentEntity(Point(0, 0))
        self.content1 = TestContentEntity(Point(0, 0))

    def test_content_added(self):
        core.change_active_scene(self.scene0)
        len_context0 = len(graphics._active_context)
        len_sorting0 = len(graphics._active_sorting)
        core.add_content_to_scene(self.scene0, self.content0)
        self.assertEqual(len(graphics._active_context) - len_context0, 1)
        self.assertEqual(len(graphics._active_sorting) - len_sorting0, 1)

    def test_content_removed(self):
        core.change_active_scene(self.scene0)
        core.add_content_to_scene(self.scene0, self.content0)
        len_context1 = len(graphics._active_context)
        len_sorting1 = len(graphics._active_sorting)
        core.remove_content_from_scene(self.scene0, self.content0)
        self.assertEqual(len(graphics._active_context) - len_context1, -1)
        self.assertEqual(len(graphics._active_sorting) - len_sorting1, -1)

    def test_context_swapping(self):
        core.change_active_scene(self.scene0)
        graphics.cache_active_context()
        # test cache save
        self.assertTrue(self.scene0 in graphics._context_cache)
        cameras, instructions = graphics._context_cache[self.scene0]
        self.assertTrue(cameras is graphics._active_cameras)
        self.assertTrue(instructions is graphics._active_context)
        # test core dismiss
        core.change_active_scene(self.scene1)
        self.assertFalse(self.scene1 in graphics._context_cache)
        self.assertFalse(cameras is graphics._active_cameras)
        self.assertFalse(instructions is graphics._active_context)
        # test core restore
        core.change_active_scene(self.scene0)
        self.assertEqual(cameras, graphics._active_cameras)
        self.assertEqual(instructions, graphics._active_context)
        # test cache clear
        graphics.clear_cache()
        self.assertFalse(self.scene0 in graphics._context_cache)

    def test_screen_setup(self):
        graphics.init_display()
        r = tuple(graphics.get_camera_setup(0))
        self.assertTrue(len(r), 1)
        r = tuple(graphics.get_camera_setup(1))
        self.assertTrue(len(r), 2)
        r = tuple(graphics.get_camera_setup(2))
        self.assertTrue(len(r), 4)


if __name__ == '__main__':
    unittest.main()
