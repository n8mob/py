import math
from unittest import TestCase


class Factorer:
    def __init__(self, n):
        self.n = n
        self.factors = {n: {} for n in range(2, n+1)}
        self.primes = [2, 3]
        self.max_factor = [math.ceil(math.sqrt(m)) for m in range(n)]

        if n < 3:
            return
        else:
            self.compute_factors()

    def compute_factors(self):
        for m, factors in self.factors.items():
            remainder = m
            for f in self.primes[self.index_of_prime_ceil[m]]:
                if remainder % f == 0:
                    factors[f] = factors[f] + 1 if f in factors else 1
                    remainder = remainder // f
            if remainder > 0:


    def index_of_max_prime_factor(self, m):
        if self.max_factor[m] > self.primes[-1]:

    @staticmethod
    def check_factorization(m, factors: {int: int}):
        return m == Factorer.calculate(factors)

    @staticmethod
    def calculate(factors: {int: int}):
        return math.prod([f ** e for f, e in factors.items()])


class TestFactorer(TestCase):
    def test_calculate_6(self):
        self.assertEqual(6, Factorer.calculate({2: 1, 3: 1}))

    def test_calculate_1(self):
        self.assertEqual(1, Factorer.calculate({}))

    def test_check_empty1(self):
        self.assertTrue(Factorer.check_factorization(1, {}))

    def test_check_empty2(self):
        self.assertFalse(Factorer.check_factorization(2, {}))

    def test_check_empty3(self):
        self.assertFalse(Factorer.check_factorization(3, {}))

    def test_check_2(self):
        self.assertTrue(Factorer.check_factorization(2, {2: 1}))

    def test_check_3(self):
        self.assertTrue(Factorer.check_factorization(3, {3: 1}))

    def test_check_4(self):
        self.assertTrue(Factorer.check_factorization(4, {2: 2}))

    def test_check_6(self):
        self.assertTrue(Factorer.check_factorization(6, {2: 1, 3: 1}))

    def test_check_9(self):
        self.assertTrue(Factorer.check_factorization(9, {3: 2}))

    def test_check_16(self):
        self.assertTrue(Factorer.check_factorization(16, {2: 4}))

    def test_check_30(self):
        self.assertTrue(Factorer.check_factorization(30, {2: 1, 3: 1, 5: 1}))

    def test_check_36(self):
        self.assertTrue(Factorer.check_factorization(36, {2: 2, 3: 2}))
