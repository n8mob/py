import unittest


class NGrammer:
  def __init__(self, n):
    self.n = n

  def count(self, text) -> dict[str, int]:
    ngrams = {}
    for i in range(len(text) - self.n + 1):
      ngram = tuple(text[i:i + self.n])
      if ngram in ngrams:
        ngrams[ngram] += 1
      else:
        ngrams[ngram] = 1

    return ngrams


class TestNGrammer(unittest.TestCase):
  def setUp(self):
    self.uut = NGrammer(2)

  def test_2gram_of_ab_is_1(self):
    text = "ab"
    expected = {('a', 'b'): 1}
    actual = self.uut.count(text)
    self.assertEqual(expected, actual)

  def test_2gram_of_abc_is_2(self):
    text = "abc"
    expected = {('a', 'b'): 1, ('b', 'c'): 1}
    actual = self.uut.count(text)
    self.assertEqual(expected, actual)

  def test_2gram_of_abcabc_is_221(self):
    text = "abcabc"
    expected = {('a', 'b'): 2, ('b', 'c'): 2, ('c', 'a'): 1}
    actual = self.uut.count(text)
    self.assertEqual(expected, actual)

  def test_3gram_of_abcabc_is_211(self):
    self.uut = NGrammer(3)
    text = "abcabc"
    expected = {('a', 'b', 'c'): 2, ('b', 'c', 'a'): 1, ('c', 'a','b'): 1}
    actual = self.uut.count(text)
    self.assertEqual(expected, actual)

  def test_3gram_of_ab_is_empty(self):
    self.uut = NGrammer(3)
    text = "ab"
    expected = {}
    actual = self.uut.count(text)
    self.assertEqual(expected, actual)

  def test_2gram_of_words(self):
    text = ['hello', 'world', 'it', 'is', 'a', 'beautiful', 'day', 'in', 'this', 'hello', 'world']
    expected = {
      ('hello', 'world'): 2,
      ('world', 'it'): 1,
      ('it', 'is'): 1,
      ('is', 'a'): 1,
      ('a', 'beautiful'): 1,
      ('beautiful', 'day'): 1,
      ('day', 'in'): 1,
      ('in', 'this'): 1,
      ('this', 'hello'): 1
    }

    actual = self.uut.count(text)
    self.assertEqual(expected, actual)


if __name__ == '__main__':
  unittest.main()
