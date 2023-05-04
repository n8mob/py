import math
from unittest import TestCase


class Factorer:
    """Finding Prime Factorizations

    """
    def __init__(self, n):
        self.n = n
        n_range = range(1, n+1)

        self.factors = {n: {} for n in n_range}
        self.primes = [2, 3]
        self.max_factor = {m: math.ceil(math.sqrt(m)) for m in self.factors.keys()}
        self.index_of_max_prime_factor = {m: -1 for m in self.factors.keys()}

        for i_p in range(len(self.primes)):
            for i_n in range(len(self.max_factor)):
                if self.primes[i_p] <= self.max_factor[i_n]:
                    self.index_of_max_prime_factor[i_n] = i_p
                else:
                    self.index_of_max_prime_factor[i_n] = -1

    def compute_factors(self):
        for m, factors in self.factors.items():
            remainder = m

            for index_of_prime in range(0, self.index_of_max_prime_factor[m]):
                prime_factor = self.primes[index_of_prime]
                if remainder % prime_factor == 0:
                    factors[prime_factor] = factors[prime_factor] + 1 if prime_factor in factors else 1
                    remainder = remainder // prime_factor
            if remainder == 0:  # factoring complete
                if not factors:  # new prime?
                    self.primes.append(m)
                    break

    def index_of_max_prime_factor(self, m):
        for i, p in enumerate(self.primes):
            if p >= m:
                return i

    @staticmethod
    def check_factorization(m, factors: {int: int}):
        return m == Factorer.calculate(factors)

    @staticmethod
    def calculate(factors: {int: int}):
        return math.prod([f ** e for f, e in factors.items()])


class TestHelperFunctions(TestCase):
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


class TestInit(TestCase):
    def test_init_factors_dictionary_with_2(self):
        f = Factorer(2)
        self.assertEqual(2, f.n)
        self.assertIsNotNone(f.factors)
        self.assertEqual(2, len(f.factors))
        self.assertIn(1, f.factors)
        self.assertIn(2, f.factors)

    def test_init_max_factors_with_2(self):
        f = Factorer(2)
        self.assertEqual([1, 2], f.max_factor)

    def test_init_max_factors_with_14(self):
        f = Factorer(14)
        self.assertEqual([1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4], f.max_factor)

    def test_init_empty_prime_indices(self):
        f = Factorer(14)
        self.assertEqual(14, len(f.index_of_max_prime_factor))


class TestCompute(TestCase):
    def test_compute_3(self):
        f = Factorer(3)

        f.compute_factors()

        self.assertEqual([1, 2, 3], list(f.factors.keys()))

        for n, factors in f.factors.items():
            self.assertIsNotNone(factors, f"{n}: factors should be a dictionary")
            self.assertGreater(0, len(factors), f"{n}: factors should not be empty")
