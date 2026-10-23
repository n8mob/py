from decimal import Decimal
import math
from typing import Union

NUMERIC_TYPES = Union[int, float, Decimal]
from unittest import TestCase

eng_names_full = {
  -12: 'pico',
  -9: 'nano',
  -6: 'micro',
  -3: 'milli',
  0: '',
  3: 'kilo',
  6: 'mega',
  9: 'giga',
  12: 'tera'}
eng_names_short = {
  -12: 'p',
  -9: 'n',
  -6: 'µ',
  -3: 'm',
  0: '',
  3: 'k',
  6: 'M',
  9: 'G',
  12: 'T'
}


def eng_exp(x, base=3):
  """Extracts the exponent for x when expressed in engineering notation"""
  x = Decimal(x)
  return base * Decimal(math.floor(x.adjusted() / base))


def eng_left(x, base=3):
  """Extracts the... "significand" (?) for x when expressed in engineering notation"""
  x = Decimal(x)
  return x / Decimal(10 ** eng_exp(x, base))


def pretty_print(x: Decimal, unit_name='bytes', base=3, use_short=False):
  """Return a human-readable string, representing the given decimal, x, in engineering notation.

  Args:
    x: The value to express in engineering notation

    unit_name: defaults to 'bytes', whatever unit you are pretty printing

    base: defaults to 3. This is used in calculating the exponent in order to clamp the value to a multiple of 3

    use_short:
        False (default): use full unit prefix names ('kilo', 'mega', etc.)
        True: use "short" prefixes ('k', 'M', etc.) instead.

  Notes: if base is 1, this method should print the value in plain scientific notation.
         However, any base other than 3 will likely result in a KeyError exception
         as the prefix names are only defined for standard engineering notations ('kilo', 'mega', 'milli', 'micro', etc.)
  """
  x = Decimal(x)
  significand = int(eng_left(x, base))
  scale = eng_exp(x, base)
  sep = '' if use_short else ' '
  symbols = eng_names_short if use_short else eng_names_full
  return f'{significand}{sep}{symbols[scale]}{unit_name}'


class EngExpTests(TestCase):
  def test_eng_exp_1000(self):
    self.assertEqual(3, eng_exp(1000))

  def test_eng_exp_100(self):
    self.assertEqual(0, eng_exp(100))

  def test_eng_exp_10(self):
    self.assertEqual(0, eng_exp(10))

  def test_eng_exp_1(self):
    self.assertEqual(0, eng_exp(1))

  def test_eng_exp_point1(self):
    self.assertEqual(-3, eng_exp(0.1))

  def test_eng_exp_0(self):
    self.assertEqual(0, eng_exp(0))

  def test_eng_exp_point001(self):
    self.assertEqual(-3, eng_exp(0.001))

  def test_eng_exp_point0006(self):
    self.assertEqual(-6, eng_exp(0.0006))

  def test_eng_exp_point000000001(self):
    self.assertEqual(-9, eng_exp(0.000000001))

  def test_eng_exp_point0000000001(self):
    self.assertEqual(-12, eng_exp(0.0000000001))


class EngLeftTests(TestCase):
  def test_eng_left_1(self):
    self.assertEqual(1, eng_left(1))

  def test_eng_left_2(self):
    self.assertEqual(2, eng_left(2))

  def test_eng_left_30(self):
    self.assertEqual(30, eng_left(30))

  def test_eng_left_4000(self):
    self.assertEqual(4, eng_left(4000))

  def test_eng_left_point005(self):
    self.assertEqual(5, eng_left(0.005))

  def test_eng_left_point0006(self):
    self.assertEqual(600, eng_left(0.0006))
