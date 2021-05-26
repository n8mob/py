from unittest import TestCase

from number_of_islands import build_square

grid = [
    ["1", "0"]
]


class TestBuild_square(TestCase):
    def test_build_square(self):
        actual = build_square(grid, 0, 0)
        self.assertEqual((0, 0), actual.coords)
        self.assertTrue(actual.is_land)

        actual2 = build_square(grid, 0, 1)
        self.assertEqual((0, 1), actual2.coords)
        self.assertFalse(actual2.island)
