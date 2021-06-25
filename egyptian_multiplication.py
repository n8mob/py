import random
from unittest import TestCase


def is_odd(n: int):
    return n & 1


def half(n: int):
    return n >> 1


def multiply(n, a):
    if n == 0 or a == 0:
        return 0

    if n == 1:
        return a

    result = multiply(half(n), a + a)

    if is_odd(n):
        result += a

    return result


class TestMultiply(TestCase):
    def test_odd_1(self):
        self.assertTrue(is_odd(1))

    def test_odd_2(self):
        self.assertFalse(is_odd(2))

    def test_half_1(self):
        self.assertEqual(0, half(1))

    def test_half_2(self):
        self.assertEqual(1, half(2))

    def test_half_789(self):
        self.assertEqual(394, half(789))

    def test_remainder_half_1235(self):
        n = 1235
        has_a_remainder = is_odd(n)
        self.assertTrue(has_a_remainder)

        half_n = half(n)
        self.assertLess(2 * half_n, n)
        self.assertEqual(617, half_n)

    def test_0_0(self):
        self.assertEqual(0, multiply(0, 0))

    def test_1_0(self):
        self.assertEqual(0, multiply(1, 0))

    def test_0_1(self):
        self.assertEqual(0, multiply(0, 1))

    def test_1_1(self):
        self.assertEqual(1, multiply(1, 1))

    def test_1_2(self):
        self.assertEqual(2, multiply(1, 2))

    def test_2_1(self):
        self.assertEqual(2, multiply(2, 1))

    def test_9_9(self):
        self.assertEqual(81, multiply(9, 9))

    def test_99_99(self):
        self.assertEqual(9_801, multiply(99, 99))

    def test_999_999(self):
        self.assertEqual(998_001, multiply(999, 999))

    def test_9999_9999(self):
        self.assertEqual(99_980_001, multiply(9999, 9999))

    def test_99999_99999(self):
        self.assertEqual(9_999_800_001, multiply(99999, 99999))

    def test_e9_e9(self):
        self.assertEqual(1_000_000_000_000_000_000, multiply(1_000_000_000, 1_000_000_000))

    def test_nine_nines(self):
        self.assertEqual(999_999_998_000_000_001, multiply(999_999_999, 999_999_999))

    def test_eleven_nines(self):
        self.assertEqual(9_999_999_999_800_000_000_001, multiply(99_999_999_999, 99_999_999_999))

    def test_without_mine(self):
        for i in range(100_000):
            n = random.randint(10_000, 100_000)
            a = random.randint(10_000, 100_000)

            self.assertEqual(n * a, n * a)

    def test_only_mine(self):
        for i in range(100_000):
            n = random.randint(10_000, 100_000)
            a = random.randint(10_000, 100_000)

            self.assertEqual(multiply(n, a), multiply(n, a))

    def test_a_bunch_of_times(self):
        for i in range(100_000):
            n = random.randint(10_000, 100_000)
            a = random.randint(10_000, 100_000)

            self.assertEqual(n * a, multiply(n, a))
