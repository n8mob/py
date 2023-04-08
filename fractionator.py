import fractions
from unittest import TestCase

GIVE_UP = 9_999_999_999
PROMPT = 'n: '


def main():
  s = input(PROMPT)
  debug = False
  if s.lower().startswith('debug'):
    debug = True
    print('debug mode')
    s = input(PROMPT)
  while not s.lower().startswith('quit'):
    n = float(s)
    if debug:
      print(f's: {s}\tn: {n}')

    fraction = fractions.Fraction.from_float(n).limit_denominator(9999999)
    print(fraction)

    s = input(PROMPT)

  print('goodbye')


def get_like_denominators(fset: {(int, int)}) -> {(int, int)}:
  if len(fset) != 2:
    raise NotImplementedError('Sorry, we can only handle two fractions for now')

  (n1, d1), (n2, d2) = fset

  newdenom = least_common_multiple(d1, d2)

  factor1 = int(newdenom / d1)
  factor2 = int(newdenom / d2)

  f1 = (n1 * factor1, newdenom)
  f2 = (n2 * factor2, newdenom)

  scaled: {int, int} = {f1, f2}

  return scaled


def least_common_multiple(a,b):
  """example: least_common_multiple(34,39) => 1326"""
  if a == b:
    return a

  if a == 0 or b == 0:
    return 0

  a = abs(a)
  b = abs(b)

  m_orig = m = min(a, b)
  n_orig = n = max(a, b)

  while m != n and n < GIVE_UP and m < GIVE_UP:
    if m < n:
      m += m_orig
    elif n < m:
      n += n_orig

  return n


if __name__ == '__main__':
    main()


class TestDenominators(TestCase):
  def test_too_few(self):
    with self.assertRaises(NotImplementedError) as actual:
      get_like_denominators({(1,2)})

    self.assertIn('two fractions', str(actual.exception))

  def test_too_many(self):
    with self.assertRaises(NotImplementedError) as actual:
      get_like_denominators({(2,3),(5,7),(11,13)})

    self.assertIn('two fractions', str(actual.exception))

  def test_third_and_half(self):
    expected = {(3,12),(4,12)}
    actual1 = get_like_denominators({(1,3),(1,4)})
    self.assertEqual(expected, actual1)
    actual2 = get_like_denominators({(1,4),(1,3)})
    self.assertEqual(expected, actual2)
    self.assertEqual(actual1,actual2)

  def test_seventh_and_tenth(self):
    expected = {(10,70),(7,70)}



class TestLcm(TestCase):
  def test_0_0(self):
    self.assertEqual(0, least_common_multiple(0,0))

  def test_0_1(self):
    self.assertEqual(0, least_common_multiple(0, 1))

  def test_1_1(self):
    self.assertEqual(1, least_common_multiple(1, 1))

  def test_2_3(self):
    self.assertEqual(6, least_common_multiple(2, 3))

  def test_34_39(self):
    self.assertEqual(1326, least_common_multiple(34, 39))

  def test_64_256(self):
    self.assertEqual(256, least_common_multiple(64, 256))

  def test_7_10(self):
    self.assertEqual(70, least_common_multiple(7, 10))
