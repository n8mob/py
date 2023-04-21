import os
import sys
from unittest import TestCase

PRIMES_TO_19 = [2, 3, 5, 7, 11, 13, 17, 19]


class Sieve:
    def __init__(self, initial_primes: [int] = None):
        if initial_primes is None:
            initial_primes = PRIMES_TO_19
        self.primes = initial_primes.copy()

    def sieve(self, n=9999):
        if n < self.primes[-1]:
            return self.primes

        nums = [n for n in range(self.primes[-1] + 2, n, 2)]

        for p in self.primes:
            if p == 2:
                continue
            i = 0
            while i < len(nums):
                if nums[i] % p == 0:
                    nums.pop(i)
                else:
                    i += 1

            if nums:
                self.primes.append(nums.pop(0))

        return self.primes + nums


class TestSieve(TestCase):
    def setUp(self) -> None:
        self.unit_under_test = Sieve(PRIMES_TO_19)
        self.diagnostic_count = 10
        self.diagnostic_lines = []

    def test_20(self):
        actual = self.unit_under_test.sieve(20)
        self.assertEqual(PRIMES_TO_19, actual)

    def test_5(self):
        actual = self.unit_under_test.sieve(5)
        self.assertEqual(PRIMES_TO_19, actual)

    def test_23(self):
        actual = self.unit_under_test.sieve(23)
        self.assertEqual(PRIMES_TO_19, actual)

    def test_24(self):
        actual = self.unit_under_test.sieve(24)
        self.assertEqual(PRIMES_TO_19 + [23], actual)

    def test_100(self):
        expected = PRIMES_TO_19 + [23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        actual = self.unit_under_test.sieve(100)

        self.check_two_arrays(expected, actual)

    def test_100_000(self):
        actual = self.unit_under_test.sieve(90_000)

        with open(os.path.expanduser('~/Downloads/primes-to-100k.txt')) as pf:
            i = 0
            for line in pf:
                p = int(line)
                self.check_ith_actual(actual, i, p)
                i += 1

    def check_two_arrays(self, expected, actual):
        if len(expected) != len(actual):
            self.assertEqual(expected, actual, "lengths already don't match")

        for i in range(len(actual)):
            self.check_ith_actual(actual, i, expected[i])

    def check_ith_actual(self, actual, i, p):
        if i > len(actual) or p != actual[i]:
            print(f'{self.diagnostic_count} from expected: {self.diagnostic_lines}')
            start = max(0, i - self.diagnostic_count)
            end = min(i+1, len(actual))
            print(f'{self.diagnostic_count} from actual: {actual[start:end]}')

        if len(self.diagnostic_lines) >= self.diagnostic_count:
            self.diagnostic_lines.pop(0)
        self.diagnostic_lines.append(p)

        self.assertLessEqual(i, len(actual), 'actual too short')
        self.assertEqual(p, actual[i], 'actual comparison')


if __name__ == '__main__':
    if not sys.argv[1] or not int(sys.argv[1]):
        print(f'usage: {sys.argv[0]} <n>')
        print('\nwhere <n> is the value up to which you want to sieve the primes')

    n_in = int(sys.argv[1])

    primes_to_n = Sieve().sieve(n_in)

    print(primes_to_n)
