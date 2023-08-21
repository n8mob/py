import random
import unittest
from datetime import datetime, timedelta

DEBUG = False


class TestPass:
    def __init__(self, number, start_time, end_time=None, swaps=0):
        self.number = number
        self.start_time = start_time
        self.end_time = end_time
        self.swaps = swaps

    def __str__(self):
        return f"| {self.number} | {self.get_elapsed()} | {self.swaps} |"

    def get_elapsed(self):
        return self.end_time - self.start_time


class SortingTestCase:
    def __init__(self, test_data, expected_elapsed, expected_passes, expected_swaps, int_size=4):
        self.test_data = self.make_ints(test_data, int_size)
        self.expected_elapsed = expected_elapsed
        self.expected_passes = expected_passes
        self.expected_swaps = expected_swaps
        self.test_passes = []

    @staticmethod
    def make_ints(test_data, int_size):
        a = []

        for i in range(0, len(test_data), int_size):
            a.append(int.from_bytes(test_data[i:i + int_size], 'little'))

        return a


class TestSorting(unittest.TestCase):
    @staticmethod
    def get_random_bytes():
        return [
            random.randbytes(1_000),
            random.randbytes(2_000),
            random.randbytes(4_000),
            random.randbytes(8_000),
            random.randbytes(16_000),
            random.randbytes(32_000),
            random.randbytes(64_000),
            random.randbytes(128_000),
            random.randbytes(256_000),
            random.randbytes(512_000)
        ]

    def setUp(self) -> None:
        self.test_arrays = TestSorting.get_random_bytes()

    def test_naive_sort(self):
        """implementing bubble sort from memory
        maybe it's actually something else, so I named the test "naive" sort
        """
        test_cases = [
            SortingTestCase(self.test_arrays[0], 125, 250, 30_000),
            SortingTestCase(self.test_arrays[1], 250, 500, 100_000),
            SortingTestCase(self.test_arrays[2], 500, 1000, 500_000),
            SortingTestCase(self.test_arrays[3], 1000, 2000, 2_000_000),
            SortingTestCase(self.test_arrays[4], 2000, 4000, 8_000_000)
        ]

        self.test_algorithm(self.naive_sort, test_cases)

    def test_merge_sort(self):
        """Gross - now I have to implement merge sort???"""
        test_cases = [
            SortingTestCase(self.test_arrays[0], 25, 4, 100),
            SortingTestCase(self.test_arrays[1], 50, 10, 1_000),
            SortingTestCase(self.test_arrays[2], 100, 100, 2_000),
            SortingTestCase(self.test_arrays[3], 200, 150, 4_000),
            SortingTestCase(self.test_arrays[4], 400, 200, 8_000)
        ]

        self.test_algorithm(self.merge_sort, test_cases)

    def test_algorithm(self, method, test_cases):
        for test_case in test_cases:
            with self.subTest(f"{len(test_case.test_data)} integers"):
                start = datetime.now()

                sort_passes = [TestPass(-1, datetime.now(), swaps=1)]
                sort_passes[0].end_time = sort_passes[0].start_time

                while sort_passes[-1].swaps > 0:
                    sort_pass = TestPass(sort_passes[-1].number + 1, datetime.now())

                    method(sort_pass, test_case)

                    sort_pass.end_time = datetime.now()

                    self.assertLessEqual(sort_pass.get_elapsed(), timedelta(milliseconds=100))
                    sort_passes.append(sort_pass)

                total_elapsed = datetime.now() - start

                elapsed_sum = timedelta(milliseconds=0)
                total_swaps = 0

                if DEBUG:
                    print('| iteration | start time | end time | elapsed | swaps | ')
                    for p in sort_passes:
                        elapsed_sum += p.get_elapsed()
                        total_swaps += p.swaps
                        print(p)

                self.assertLessEqual(elapsed_sum, total_elapsed)

                self.assertLessEqual(total_elapsed, timedelta(milliseconds=test_case.expected_elapsed), 'elapsed')
                self.assertLessEqual(len(sort_passes), test_case.expected_passes, 'passes')
                self.assertLessEqual(sum((p.swaps for p in sort_passes)), test_case.expected_swaps, 'swaps')

    @staticmethod
    def naive_sort(sort_pass, test_case):
        for i in range(len(test_case.test_data) - 1):
            if test_case.test_data[i] < test_case.test_data[i + 1]:
                tmp = test_case.test_data[i]
                test_case.test_data[i] = test_case.test_data[i + 1]
                test_case.test_data[i + 1] = tmp
                sort_pass.swaps += 1

    @staticmethod
    def merge_sort(sort_pass, test_case):
        pass

    def merge_sort_segment(self, a, b):
        a_a, a_b = self.partition(a)
        b_a, b_b = self.partition(b)



    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
