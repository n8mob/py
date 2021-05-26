from unittest import TestCase

from number_of_islands import Solution

case1 = [
    ["1", "1", "1", "1", "0"],
    ["1", "1", "0", "1", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "0", "0", "0"]
]

case2 = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"],
]

case3 = [
    ["1", "1", "1"],
    ["0", "1", "0"],
    ["1", "1", "1"]
]


class TestSolution(TestCase):
    def setUp(self) -> None:
        self.subject = Solution()

    def test_case1(self):
        result = self.subject.numIslands(case1)
        self.assertEqual(1, result)

    def test_case2(self):
        result = self.subject.numIslands(case2)
        self.assertEqual(3, result)

    def test_case3(self):
        result = self.subject.numIslands(case3)
        self.assertEqual(1, result)
