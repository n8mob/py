import math
import random
import unittest
from datetime import datetime, timedelta
from math import floor

DEBUG = True


class TestPass:
    def __init__(self, number, start_time, end_time=None, details=None):
        self.number = number
        self.start_time = start_time
        self.end_time = end_time
        self.details = details or {}

    def __str__(self):
        return f"| {self.number} | {self.get_elapsed()} | {self.get_primary_detail()} |"

    def get_elapsed(self) -> timedelta:
        return self.end_time - self.start_time

    def get_primary_detail(self):
        if 'swaps' in self.details:
            return {'swaps': self.details['swaps']}
        else:
            for detail, value in self.details.items():
                if value is not None:
                    return {detail: value}


class SortingTestCase:
    def __init__(self, test_data, expected_details: dict = None, int_size=4):
        self.test_data = self.make_ints(test_data, int_size)
        self.expected_details = expected_details or {}
        self.test_passes = []

    @staticmethod
    def make_ints(test_data, int_size):
        a = []

        for i in range(0, len(test_data), int_size):
            a.append(int.from_bytes(test_data[i:i + int_size], 'little'))

        return a


class TestSorting(unittest.TestCase):
    def setUp(self) -> None:
        self.test_arrays = [
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

    def test_naive_sort(self):
        test_cases = [
            SortingTestCase(self.test_arrays[0], {
                'total_elapsed': timedelta(milliseconds=125),
                'pass_elapsed': timedelta(milliseconds=150),
                'passes': 251,
                'swaps': 20_000}),
            SortingTestCase(self.test_arrays[1], {
                'total_elapsed': timedelta(milliseconds=250),
                'pass_elapsed': timedelta(milliseconds=300),
                'passes': 501,
                'swaps': 2_000_000}),
            SortingTestCase(self.test_arrays[2], {
                'total_elapsed': timedelta(milliseconds=500),
                'pass_elapsed': timedelta(milliseconds=500),
                'passes': 1001,
                'swaps': 4_000_000})
        ]

        def keep_testing(test_case: SortingTestCase, previous: TestPass):
            if previous.number > test_case.expected_details['passes']:
                return False
            if 'swaps' in previous.details:
                return previous.details['swaps'] > 0
            return True

        self.algorithm_test_helper(self.naive_sort, test_cases, keep_testing)

    def test_merge_sort(self):
        test_cases = [
            SortingTestCase(self.test_arrays[6], {'total_elapsed': timedelta(milliseconds=500)}),
            SortingTestCase(self.test_arrays[7], {'total_elapsed': timedelta(milliseconds=1000)}),
            SortingTestCase(self.test_arrays[8], {'total_elapsed': timedelta(milliseconds=2000)}),
            SortingTestCase(self.test_arrays[9], {'total_elapsed': timedelta(milliseconds=5000)})
        ]

        self.algorithm_test_helper(self.merge_sort, test_cases, lambda test_case, previous: previous.number < 2)

    def algorithm_test_helper(self, method, test_cases, keep_testing):
        for test_case in test_cases:
            with self.subTest(f"{len(test_case.test_data)} integers"):
                start = datetime.now()

                sort_passes = [TestPass(-1, datetime.now(), {'swaps': 1})]
                sort_passes[0].end_time = sort_passes[0].start_time

                while keep_testing(test_case, sort_passes[-1]):
                    sort_pass = TestPass(sort_passes[-1].number + 1, datetime.now())

                    method(sort_pass, test_case)

                    sort_pass.end_time = datetime.now()

                    if 'pass_elapsed' in test_case.expected_details:
                        expected = test_case.expected_details['pass_elapsed']
                        actual = sort_pass.get_elapsed()
                        self.assertLessEqual(actual, expected, msg=f"test pass {sort_pass.number} took too long")
                    sort_passes.append(sort_pass)

                elapsed_sum = timedelta(milliseconds=0)
                details = {'total_elapsed': (datetime.now() - start)}

                if DEBUG:
                    print('| iteration | start time | end time | details | ')

                for p in sort_passes:
                    elapsed_sum += p.get_elapsed()
                    for detail in p.details:
                        if detail not in details:
                            details[detail] = 1
                        details[detail] += p.details[detail]
                    if DEBUG:
                        print(p)

                self.assertLessEqual(elapsed_sum, datetime.now() - start)

                for detail in test_case.expected_details:
                    if detail in details:
                        self.assertLessEqual(
                            details[detail],
                            test_case.expected_details[detail],
                            f'{detail} not less than or equal to expectation'
                        )

    @staticmethod
    def naive_sort(sort_pass: TestPass, test_case):
        for i in range(len(test_case.test_data) - 1):
            if test_case.test_data[i] > test_case.test_data[i + 1]:
                tmp = test_case.test_data[i]
                test_case.test_data[i] = test_case.test_data[i + 1]
                test_case.test_data[i + 1] = tmp
                if 'swaps' not in sort_pass.details:
                    sort_pass.details['swaps'] = 1
                else:
                    sort_pass.details['swaps'] += 1

    def merge_sort(self, sort_pass, test_case):
        self.merge_sort_segment(test_case.test_data)

    def merge_sort_segment(self, a):
        if len(a) < 2:
            return a

        p = floor(len(a) / 2)

        return self.merge(self.merge_sort_segment(a[:p]), self.merge_sort_segment(a[p:]))

    @staticmethod
    def merge(a, b):
        if not a and not b:
            return []
        elif not a:
            return b
        elif not b:
            return a

        merged = []

        while a and b:
            if a[0] <= b[0]:
                merged.append(a.pop(0))
            else:
                merged.append(b.pop(0))

        if b:
            return merged + b
        else:
            return merged + a

    def test_merge_nones(self):
        self.assertEqual([], self.merge(None, None))
        self.assertEqual([], self.merge([], None))
        self.assertEqual([], self.merge(None, []))
        self.assertEqual([], self.merge([], []))
        self.assertEqual([1], self.merge([1], None))
        self.assertEqual([1], self.merge(None, [1]))

    def test_merge_0to1(self):
        self.assertEqual([1], self.merge([1], []))
        self.assertEqual([1], self.merge([], [1]))
        self.assertEqual([1, 1], self.merge([1], [1]))
        self.assertEqual([1, 2], self.merge([1], [2]))
        self.assertEqual([1, 2], self.merge([2], [1]))

    def test_merge_1to2(self):
        self.assertEqual([1, 1, 2], self.merge([1], [1, 2]))
        self.assertEqual([1, 2, 3], self.merge([1], [2, 3]))
        self.assertEqual([1, 2, 3], self.merge([1, 2], [3]))
        self.assertEqual([1, 2, 3], self.merge([1, 3], [2]))
        self.assertEqual([1, 2, 3, 4], self.merge([1, 2], [3, 4]))
        self.assertEqual([1, 2, 3, 4], self.merge([1, 3], [2, 4]))

    def test_length_differs_by_2(self):
        self.assertEqual([1, 2, 3, 4, 5, 6], self.merge([1, 2], [3, 4, 5, 6]))
        self.assertEqual([1, 2, 3, 4, 5, 6], self.merge([1, 2, 3, 4], [5, 6]))
        self.assertEqual([1, 2, 3, 4, 5, 6], self.merge([1, 4], [2, 3, 5, 6]))
        self.assertEqual([1, 2, 3, 4, 5, 6], self.merge([1, 6], [2, 3, 4, 5]))
        self.assertEqual([1, 2, 3, 4, 5, 6], self.merge([2, 3, 4, 5], [1, 6]))


if __name__ == '__main__':
    unittest.main()
