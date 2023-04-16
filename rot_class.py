import string
from unittest import TestCase


class Rot:
    @staticmethod
    def aZero(c):
        return ord(c.upper()) - ord('A')

    @staticmethod
    def zeroA(n):
        return chr(n + ord('A'))

    def stringFromInts(self, l, n=0):
        return ''.join(self.zeroA(c + n) for c in l)

    def intsFromString(self, st, n=0):
        return [self.aZero(c) if c in string.ascii_letters else '' for c in st]

    def rotChar(self, n, m, c):
        num = (self.aZero(c) + n) % m
        return self.zeroA(num)

    @staticmethod
    def rotInts(n, m, l):
        return [(i + n) % m for i in l]

    def rot(self, n, m, st):
        return ''.join(self.rotChar(n, m, c) for c in st)

    def bruteRot(self, m, st):
        return [self.rot(n, m, st) for n in range(1, m)]

    def applyKey(self, key, text, m=26):
        keyLen = len(key)
        txtLen = len(text)
        chunkSize = min(keyLen, txtLen)

        transformedText = ''

        chunks = [text[i:i + chunkSize] for i in range(0, len(text), chunkSize)]
        for chunk in chunks:
            for i in range(0, min(chunkSize, len(chunk))):
                transformedText += self.rotChar(self.aZero(key[i]), m, chunk[i])

        return transformedText


class TestAZero(TestCase):
    def setUp(self):
        self.unit_under_test = Rot()

    def test_cIs2(self):
        self.assertEqual(2, self.unit_under_test.aZero('c'))

    def test_zIs25(self):
        self.assertEqual(25, self.unit_under_test.aZero('z'))

    def test_yIs24(self):
        self.assertEqual(24, self.unit_under_test.aZero('y'))


class TestZeroA(TestCase):
    def setUp(self) -> None:
        self.unit_under_test = Rot()

    def test_4IsE(self):
        self.assertEqual('E', self.unit_under_test.zeroA(4))

    def test_25IsZ(self):
        self.assertEqual('Z', self.unit_under_test.zeroA(25))

    def test_CaseInsensitiveRoundTrip(self):
        self.assertEqual('Z', self.unit_under_test.zeroA(self.unit_under_test.aZero('z')))


class TestRestOfRot(TestCase):
    def setUp(self) -> None:
        self.unit_under_test = Rot()

    def test_azInts(self):
        self.assertEqual([0, 25], self.unit_under_test.intsFromString('az'))

    def test_rotAby13(self):
        self.assertEqual('N', self.unit_under_test.rotChar(13, 26, 'a'))

    def test_rotNby13(self):
        self.assertEqual('A', self.unit_under_test.rotChar(13, 26, 'n'))

    def test_rotYby1(self):
        self.assertEqual('Z', self.unit_under_test.rotChar(1, 26, 'y'))

    def test_rotAlphabetBy1(self):
        rot1alphabet = 'BCDEFGHIJKLMNOPQRSTUVWXYZA'
        self.assertEqual(rot1alphabet, self.unit_under_test.rot(1, 26, string.ascii_lowercase))

    def test_rotAlphabetBy13(self):
        rot13alphabet = 'NOPQRSTUVWXYZABCDEFGHIJKLM'
        self.assertEqual(rot13alphabet, self.unit_under_test.rot(13, 26, string.ascii_lowercase))

    def test_applyKeyBBB(self):
        self.assertEqual('BCD', self.unit_under_test.applyKey('bbb', 'abc'))

    def test_applyKeyB(self):
        self.assertEqual('BC', self.unit_under_test.applyKey('b', 'ab'))

    def test_applyKeyBC(self):
        self.assertEqual('CD', self.unit_under_test.applyKey('bc', 'bb'))
