from api.utilities.vector import *

import unittest


class VectorTest(unittest.TestCase):

    def setUp(self):
        self.v00 = Vector2(0, 0)
        self.v10 = Vector2(5, 0)
        self.v01 = Vector2(0, 3)
        self.v11 = Vector2(1, 1)

    def test_lenq(self):
        self.assertTrue(2 == v_lenq(self.v11))

    def test_len(self):
        self.assertTrue(5 == v_len(self.v10))
        self.assertTrue(3 == v_len(self.v01))

    def test_dot(self):
        self.assertFalse(0 == v_dot(self.v10, self.v11))
        self.assertFalse(0 == v_dot(self.v01, self.v11))
        self.assertFalse(0 == v_dot(self.v01, self.v01))
        self.assertFalse(0 == v_dot(self.v10, self.v10))
        self.assertFalse(0 == v_dot(self.v11, self.v11))
        self.assertTrue(0 == v_dot(self.v01, self.v10))

    def test_add(self):
        x1, y1 = Vector2(6, 4)
        x2, y2 = v_add(self.v00, self.v01, self.v10, self.v11)
        self.assertTrue(x1 == x2 and y1 == y2)

    def test_sub(self):
        x1, y1 = Vector2(-6, -4)
        x2, y2 = v_sub(self.v00, self.v01, self.v10, self.v11)
        self.assertTrue(x1 == x2 and y1 == y2)

    def test_mul(self):
        x1, y1 = Vector2(0, 0)
        x2, y2 = v_mul(self.v00, self.v11)
        self.assertTrue(x1 == x2 and y1 == y2)
        x2, y2 = v_mul(self.v01, self.v10)
        self.assertTrue(x1 == x2 and y1 == y2)
        x1, y1 = Vector2(10, 10)
        x2, y2 = v_mul(self.v11, 10)
        self.assertTrue(x1 == x2 and y1 == y2)
        x2, y2 = v_mul(self.v11, 10.0)
        self.assertTrue(x1 == x2 and y1 == y2)

    def test_div(self):
        x1, y1 = Vector2(0, 0)
        x2, y2 = v_div(self.v00, self.v11)
        self.assertTrue(x1 == x2 and y1 == y2)
        x1, y1 = Vector2(0, 3)
        x2, y2 = v_mul(self.v01, self.v11)
        self.assertTrue(x1 == x2 and y1 == y2)
        x1, y1 = Vector2(0.5, 0.5)
        x2, y2 = v_div(self.v11, 2)
        self.assertTrue(x1 == x2 and y1 == y2)
        x2, y2 = v_div(self.v11, 2.0)
        self.assertTrue(x1 == x2 and y1 == y2)

        v1 = Vector2(1, 1)
        v2 = Vector2(2, 2)
        x1, y1 = Vector2(0.5, 0.5)
        x2, y2 = v_div(v1, v2)
        self.assertTrue(x1 == x2 and y1 == y2, "{},{}".format(x2, y2))

        v2 = Vector2(60, 33.75)
        x1, y1 = Vector2(1/60, 1/33.75)
        x2, y2 = v_div(v1, v2)
        self.assertTrue(x1 == x2 and y1 == y2, "{},{}".format(x2, y2))

    def test_min(self):
        x1, y1 = Vector2(0, 0)
        x2, y2 = v_min(self.v00, self.v11)
        self.assertTrue(x1 == x2 and y1 == y2)
        x2, y2 = v_min(self.v10, self.v01)
        self.assertTrue(x1 == x2 and y1 == y2)

    def test_max(self):
        x1, y1 = Vector2(1, 1)
        x2, y2 = v_max(self.v00, self.v11)
        self.assertTrue(x1 == x2 and y1 == y2)
        x1, y1 = Vector2(5, 3)
        x2, y2 = v_max(self.v10, self.v01)
        self.assertTrue(x1 == x2 and y1 == y2)

    def test_norm(self):
        x1, y1 = Vector2(1, 0)
        x2, y2 = v_norm(self.v10)
        self.assertTrue(x1 == x2 and y1 == y2)
        x1, y1 = Vector2(0, 1)
        x2, y2 = v_norm(self.v01)
        self.assertTrue(x1 == x2 and y1 == y2)


if __name__ == '__main__':
    unittest.main()
