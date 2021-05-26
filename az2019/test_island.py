from unittest import TestCase

from number_of_islands import Island

a = 0, 0
b = 1, 0
c = 2, 0
d = 3, 0
e = 4, 0

f = 0, 1
g = 1, 1
h = 2, 1
i = 3, 1
j = 4, 1


class TestIsland(TestCase):
    def test_are_neighbors(self):
        self.assertTrue(Island.are_neighbors(a, b))
        self.assertTrue(Island.are_neighbors(b, c))
        self.assertFalse(Island.are_neighbors(a, c))

    def test_not_share_neighbors(self):
        island_a = Island(a)
        island_j = Island(j)

        self.assertFalse(Island.share_neighbors(island_a, island_j))

    def test_shared_neighbors(self):
        island_a = Island(a)
        island_b = Island(b)

        self.assertTrue(Island.share_neighbors(island_a, island_b))

