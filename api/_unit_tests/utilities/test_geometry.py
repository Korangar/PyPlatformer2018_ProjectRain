import unittest
from api.utilities.geometry import *


class GeometryTest(unittest.TestCase):
    def test_rect2rect(self):
        b = Rectangle(Point(0, 0), Vector2(2, 2))
        self.assertTrue(b.intersect(b))
        b1 = Rectangle(Point(1, 1), Vector2(2, 2))
        self.assertTrue(b.intersect(b1))
        b2 = Rectangle(Point(2, 2), Vector2(2, 2))
        self.assertTrue(b.intersect(b2))
        b3 = Rectangle(Point(2.1, 2.1), Vector2(2, 2))
        self.assertFalse(b.intersect(b3))
        b4 = Rectangle(Point(1, 1), Vector2(-2, -2))
        self.assertTrue(b.intersect(b4))
        b5 = Rectangle(Point(2, 2), Vector2(-2, -2))
        self.assertTrue(b.intersect(b5))
        b6 = Rectangle(Point(0, 0), Vector2(-2, -2))
        self.assertTrue(b.intersect(b6))
        b7 = Rectangle(Point(-.1, -.1), Vector2(-2, -2))
        self.assertFalse(b.intersect(b7))

    def test_rect2ray(self):
        b = Rectangle(Point(0, 0), Vector2(2, 2))
        r1 = create_ray(Point(-1, -1), Vector2(1, 1))
        self.assertTrue(b.intersect(r1))
        r2 = create_ray(Point(1, 1), Vector2(3, 3))
        self.assertTrue(b.intersect(r2))
        r3 = create_ray(Point(0, 0), Vector2(2, 2))
        self.assertTrue(b.intersect(r3))
        r4 = create_ray(Point(-1, -1), Vector2(3, 3))
        self.assertTrue(b.intersect(r4))
        r5 = create_ray(Point(-1, 0), Vector2(1, 0), 0.99)
        self.assertFalse(b.intersect(r5))
        r6 = create_ray(Point(3, 0), Vector2(-1, 0), 0.99)
        self.assertFalse(b.intersect(r6))
        r7 = create_ray(Point(-1, 1), Vector2(0, -1))
        self.assertFalse(b.intersect(r7))
        r8 = create_ray(Point(-1, 1), Vector2(1, -1))
        self.assertTrue(b.intersect(r8))
        r9 = create_ray(Point(-1, 1), Vector2(2, -1))
        self.assertTrue(b.intersect(r9))

    def test_rect2circle(self):
        b = Rectangle(Point(0, 0), Vector2(2, 2))
        c1 = Circle(Point(1, 1), 1)
        self.assertTrue(b.intersect(c1))
        c2 = Circle(Point(1, 1), 5)
        self.assertTrue(b.intersect(c2))
        c3 = Circle(Point(0, 0), 1)
        self.assertTrue(b.intersect(c3))
        c4 = Circle(Point(-1, 1), 1)
        self.assertTrue(b.intersect(c4))
        c5 = Circle(Point(-1, 1), 0.99)
        self.assertFalse(b.intersect(c5))
        c6 = Circle(Point(3, 3), math.sqrt(2))
        self.assertTrue(b.intersect(c6))
        c7 = Circle(Point(3.01, 3.01), math.sqrt(2))
        self.assertFalse(b.intersect(c7))

    def test_rect2point(self):
        b = Rectangle(Point(0, 0), Vector2(2, 2))
        p1 = Point(1, 1)
        self.assertTrue(b.intersect(p1))
        p2 = Point(0, 0)
        self.assertTrue(b.intersect(p2))
        p3 = Point(2, 2)
        self.assertTrue(b.intersect(p3))
        p4 = Point(-.1, 1)
        self.assertFalse(b.intersect(p4))
        p5 = Point(3, 1)
        self.assertFalse(b.intersect(p5))


if __name__ == '__main__':
    unittest.main()
