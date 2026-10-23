import string
import sys
import unittest
from unittest import TestCase


class Rot:
  @staticmethod
  def a_zero(c):
    return ord(c.upper()) - ord('A')

  @staticmethod
  def zero_a(n):
    return chr(n + ord('A'))

  def string_from_ints(self, l, n=0):
    return ''.join(self.zero_a(c + n) for c in l)

  def ints_from_string(self, st, n=0):
    return [self.a_zero(c) if c in string.ascii_letters else '' for c in st]

  def rot_char(self, n, m, c, retain_space = True):
    encoded = self.a_zero(c)
    if retain_space and encoded not in range (0, m):
      return c

    num = (encoded + n) % m
    return self.zero_a(num)

  @staticmethod
  def rot_ints(rot_dist, mod_len, ints):
    return [(n + rot_dist) % mod_len for n in ints]

  def rot_string(self, rot_dist, mod_len, s):
    return ''.join(self.rot_char(rot_dist, mod_len, c) for c in s)

  def brute_rot(self, mod_len, s):
    return [self.rot_string(n, mod_len, s) for n in range(1, mod_len)]

  def apply_key(self, key, text, m=26):
    key_len = len(key)
    txt_len = len(text)
    chunk_size = min(key_len, txt_len)

    transformed = ''

    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    for chunk in chunks:
      for i in range(0, min(chunk_size, len(chunk))):
        transformed += self.rot_char(self.a_zero(key[i]), m, chunk[i])

    return transformed

  def interactive_brute_rot(self, st):
    for i in range(26, 0, -1):
      candidate = self.rot_string(i, 26, st)
      is_solution = input(candidate + ' ? y/N')
      if is_solution.lower() in ['', 'n']:
        continue
      else:
        print(f'\n{st} rotated by {i} is {candidate}\n')
        break


class TestAZero(TestCase):
  def setUp(self):
    self.unit_under_test = Rot()

  def test_cIs2(self):
    self.assertEqual(2, self.unit_under_test.a_zero('c'))

  def test_zIs25(self):
    self.assertEqual(25, self.unit_under_test.a_zero('z'))

  def test_yIs24(self):
    self.assertEqual(24, self.unit_under_test.a_zero('y'))

  def test_space(self):
    self.assertEqual(-33, self.unit_under_test.a_zero(' '))


class TestZeroA(TestCase):
  def setUp(self) -> None:
    self.unit_under_test = Rot()

  def test_4IsE(self):
    self.assertEqual('E', self.unit_under_test.zero_a(4))

  def test_25IsZ(self):
    self.assertEqual('Z', self.unit_under_test.zero_a(25))

  def test_CaseInsensitiveRoundTrip(self):
    self.assertEqual('Z', self.unit_under_test.zero_a(self.unit_under_test.a_zero('z')))


# noinspection SpellCheckingInspection
class TestRestOfRot(TestCase):
  def setUp(self) -> None:
    self.unit_under_test = Rot()

  def test_azInts(self):
    self.assertEqual([0, 25], self.unit_under_test.ints_from_string('az'))

  def test_rotAby13(self):
    self.assertEqual('N', self.unit_under_test.rot_char(13, 26, 'a'))

  def test_rotNby13(self):
    self.assertEqual('A', self.unit_under_test.rot_char(13, 26, 'n'))

  def test_rotYby1(self):
    self.assertEqual('Z', self.unit_under_test.rot_char(1, 26, 'y'))

  def test_retainSpace(self):
    self.assertEqual(' ', self.unit_under_test.rot_char(13, 26, ' '))
    self.assertEqual(' ', self.unit_under_test.rot_char(1, 26, ' '))

  def test_doNotRetainSpace(self):
    self.assertEqual('U', self.unit_under_test.rot_char(1, 26, ' ', retain_space=False))
    self.assertEqual('Y', self.unit_under_test.rot_char(5, 26, ' ', retain_space=False))
    self.assertEqual('Z', self.unit_under_test.rot_char(6, 26, ' ', retain_space=False))
    self.assertEqual('A', self.unit_under_test.rot_char(7, 26, ' ', retain_space=False))
    self.assertEqual('B', self.unit_under_test.rot_char(8, 26, ' ', retain_space=False))

  def test_rotAlphabetBy1(self):
    rot1alphabet = 'BCDEFGHIJKLMNOPQRSTUVWXYZA'
    self.assertEqual(rot1alphabet, self.unit_under_test.rot_string(1, 26, string.ascii_lowercase))

  def test_rotAlphabetBy13(self):
    rot13alphabet = 'NOPQRSTUVWXYZABCDEFGHIJKLM'
    self.assertEqual(rot13alphabet, self.unit_under_test.rot_string(13, 26, string.ascii_lowercase))

  def test_rotStringWithSpace(self):
    self.assertEqual('C D', self.unit_under_test.rot_string(2, 26, 'a b'))

  def test_applyKeyBBB(self):
    self.assertEqual('BCD', self.unit_under_test.apply_key('bbb', 'abc'))

  def test_applyKeyB(self):
    self.assertEqual('BC', self.unit_under_test.apply_key('b', 'ab'))

  def test_applyKeyBC(self):
    self.assertEqual('CD', self.unit_under_test.apply_key('bc', 'bb'))


if __name__ == '__main__':
  rot = Rot()
  dont_quit = True
  while dont_quit:
    inpt = input('Enter a string to ROT (or "QUIT" to quit): ')
    if inpt.upper() == 'QUIT':
      dont_quit = False
      sys.exit(0)
    print(rot.rot_string(1, 26, inpt))
