import math
import os
from datetime import datetime
from unittest import TestCase


class Factorer:
    """Finding Prime Factorizations

    """

    def __init__(self, n):
        self.n = n
        n_range = range(2, n + 1)

        self.factors = {n: {} for n in n_range}
        self.primes = [2, 3]
        self.max_factor = {m: math.ceil(math.sqrt(m)) for m in self.factors.keys()}

    def compute_factors(self):
        for m, factors in self.factors.items():
            remainder = m

            for p in self.primes:
                while remainder % p == 0:
                    factors[p] = factors[p] + 1 if p in factors else 1
                    remainder = remainder // p
            if not Factorer.check_factorization(m, factors):  # new prime?
                self.primes.append(m)
                factors[m] = 1

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

    @staticmethod
    def print_factor_line(m: int, factors: {int: {int: int}}) -> str:
        expression = ''
        for factor, power in factors.items():
            if expression != '':
                expression += '*'
            expression += str(factor)
            if power > 1:
                expression += f'^{power}'
        fs = f'| {m:>3} | {expression:<9} |'
        return fs


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
        self.assertEqual(1, len(f.factors))
        self.assertIn(2, f.factors)

    def test_init_max_factors_with_2(self):
        f = Factorer(2)
        self.assertEqual({2: 2}, f.max_factor)

    def test_init_max_factors_with_14(self):
        f = Factorer(14)
        self.assertEqual([2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4], list(f.max_factor.values()))

class TestCompute(TestCase):
    def test_compute_3(self):
        f = Factorer(3)

        f.compute_factors()

        self.assertIn(2, f.factors)
        self.assertIn(3, f.factors)

        self.assertEqual({2: 1}, f.factors[2])
        self.assertEqual({3: 1}, f.factors[3])

        for m, factors in f.factors.items():
            self.assertIsNotNone(factors, f"{m}: factors should be a dictionary")
            self.assertGreater(len(factors), 0, f"{m}: factors should not be empty")

            self.assertTrue(f.check_factorization(m, factors))

    def test_compute_4(self):
        f = Factorer(4)

        expected_factors = {2: {2: 1},
                            3: {3: 1},
                            4: {2: 2}}

        f.compute_factors()

        self.assertEqual(expected_factors, f.factors)

        for m, factors in f.factors.items():
            self.assertTrue(f.check_factorization(m, factors))

    def test_5_detected_as_new_prime(self):
        f = Factorer(5)

        expected_factors = {2: {2: 1},
                            3: {3: 1},
                            4: {2: 2},
                            5: {5: 1}}

        f.compute_factors()

        self.assertEqual(expected_factors, f.factors)

    def test_6_has_two_factors(self):
        f = Factorer(6)
        f.compute_factors()

        self.assertEqual({2: 1, 3: 1}, f.factors[6])

    def test_12_factors_include_a_square(self):
        f = Factorer(12)
        f.compute_factors()

        expected = {2: {2: 1},
                    3: {3: 1},
                    4: {2: 2},
                    5: {5: 1},
                    6: {2: 1, 3: 1},
                    7: {7: 1},
                    8: {2: 3},
                    9: {3: 2},
                    10: {2: 1, 5: 1},
                    11: {11: 1},
                    12: {2: 2, 3: 1}}

        self.assertEqual(expected, f.factors)

    def test_up_to_20(self):
        f = Factorer(20)
        f.compute_factors()

        expected = {2: {2: 1},
                    3: {3: 1},
                    4: {2: 2},
                    5: {5: 1},
                    6: {2: 1, 3: 1},
                    7: {7: 1},
                    8: {2: 3},
                    9: {3: 2},
                    10: {2: 1, 5: 1},
                    11: {11: 1},
                    12: {2: 2, 3: 1},
                    13: {13: 1},
                    14: {2: 1, 7: 1},
                    15: {3: 1, 5: 1},
                    16: {2: 4},
                    17: {17: 1},
                    18: {2: 1, 3: 2},
                    19: {19: 1},
                    20: {2: 2, 5: 1}
                    }

        self.assertEqual(expected, f.factors)

    def test_up_to_100(self):
        f = Factorer(100)
        f.compute_factors()

        for m, factors in f.factors.items():
            self.assertTrue(Factorer.check_factorization(m, factors))

    def test_up_to_392(self):
        f = Factorer(390)
        f.compute_factors()

        with open(os.path.expanduser('~/Documents/n/projects/PrimeFactorization.org')) as pf:
            file_lines = pf.read().splitlines()[4:395]

        line_num = 0

        errors = []

        for m, factors in f.factors.items():
            fs = Factorer.print_factor_line(factors, m)
            if fs != file_lines[line_num]:
                errors.append(m)
            line_num += 1

        self.assertFalse(errors, f'\nCheck factorization of: {errors}')


if __name__ == '__main__':
    main_factorer = Factorer(392)
    main_factorer.compute_factors()

    lines = []
    for n, n_factors in main_factorer.factors.items():
        lines.append(Factorer.print_factor_line(n, n_factors) + '\n')

    with open(f'/tmp/{datetime.now()}.org', 'w') as tempfile:
        tempfile.writelines(lines)
