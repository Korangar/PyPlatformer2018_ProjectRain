from ...utilities.geometry import Point
from ...graphics.instruction import graphics_instruction

import api.graphics.system as graphics_system
import api.scene as scene_system

import unittest


class TestContent(scene_system.SceneContent):
    def __init__(self, position: Point) -> None:
        super().__init__(position)


@graphics_instruction(TestContent)
class ExampleContentGraphics(graphics_system.GraphicsInstruction[TestContent]):
    def draw(self, camera) -> None:
        pass


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.scene0 = scene_system.SceneObject()
        self.scene1 = scene_system.SceneObject()
        self.content0 = TestContent(Point(0, 0))
        self.content1 = TestContent(Point(0, 0))

    def test_content_added(self):
        scene_system.change_active_scene(self.scene0)
        len_context0 = len(graphics_system._active_context)
        len_sorting0 = len(graphics_system._active_sorting)
        scene_system.add_content_to_scene(self.scene0, self.content0)
        self.assertEqual(len(graphics_system._active_context) - len_context0, 1)
        self.assertEqual(len(graphics_system._active_sorting) - len_sorting0, 1)

    def test_content_removed(self):
        scene_system.change_active_scene(self.scene0)
        scene_system.add_content_to_scene(self.scene0, self.content0)
        len_context1 = len(graphics_system._active_context)
        len_sorting1 = len(graphics_system._active_sorting)
        scene_system.remove_content_from_scene(self.scene0, self.content0)
        self.assertEqual(len(graphics_system._active_context) - len_context1, -1)
        self.assertEqual(len(graphics_system._active_sorting) - len_sorting1, -1)

    def test_context_swapping(self):
        scene_system.change_active_scene(self.scene0)
        graphics_system.cache_active_context()
        # test cache save
        self.assertTrue(self.scene0 in graphics_system._context_cache)
        cameras, instructions = graphics_system._context_cache[self.scene0]
        self.assertTrue(cameras is graphics_system._active_cameras)
        self.assertTrue(instructions is graphics_system._active_context)
        # test scene dismiss
        scene_system.change_active_scene(self.scene1)
        self.assertFalse(self.scene1 in graphics_system._context_cache)
        self.assertFalse(cameras is graphics_system._active_cameras)
        self.assertFalse(instructions is graphics_system._active_context)
        # test scene restore
        scene_system.change_active_scene(self.scene0)
        self.assertEqual(cameras, graphics_system._active_cameras)
        self.assertEqual(instructions, graphics_system._active_context)
        # test cache clear
        graphics_system.clear_cache()
        self.assertFalse(self.scene0 in graphics_system._context_cache)


if __name__ == '__main__':
    unittest.main()
