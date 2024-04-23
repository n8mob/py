from unittest import TestCase

from phone_spell import PhoneSpell


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
