import sys
from unittest import TestCase


class PhoneSpell:
  LETTERS = {
    'A': '2',
    'B': '2',
    'C': '2',
    'D': '3',
    'E': '3',
    'F': '3',
    'G': '4',
    'H': '4',
    'I': '4',
    'J': '5',
    'K': '5',
    'L': '5',
    'M': '6',
    'N': '6',
    'O': '6',
    'P': '7',
    'Q': '7',
    'R': '7',
    'S': '7',
    'T': '8',
    'U': '8',
    'V': '8',
    'W': '9',
    'X': '9',
    'Y': '9',
    'Z': '9'
  }
  def spell(self, word):
    number = ''
    for letter in word.upper():
      number += self.LETTERS.get(letter, letter)
    return number


class TestPhoneSpell(TestCase):
  def setUp(self):
    self.unit = PhoneSpell()

  def test_empty_string(self):
    actual = self.unit.spell('')
    self.assertEqual(actual, '')

  def test_no_numbers(self):
    original = '$%^'
    actual = self.unit.spell(original)
    self.assertEqual(actual, original)

  def test_numbers_not_letters(self):
    original = '12345'
    actual = self.unit.spell(original)
    self.assertEqual(actual, original)

  def test_with_dash(self):
    number_with_dash = '599-NATE'
    actual = self.unit.spell(number_with_dash)
    self.assertEqual(actual, '599-6283')


if __name__ == '__main__':
  ps = PhoneSpell()
  ps.spell(sys.argv[0])