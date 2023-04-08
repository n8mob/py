import string
from unittest import TestCase


# noinspection PyMethodMayBeStatic
class Rot:
    def aZero(self, c):
        return ord(c.upper()) - ord('A')

    def zeroA(self, n):
        return chr(n + ord('A'))

    def stringFromInts(self, l, n=0):
        return ''.join(self.zeroA(c + n) for c in l)

    def intsFromString(self, st, n=0):
        return [self.aZero(c) if c in string.ascii_letters else '' for c in st]

    def rotChar(self, n, m, c):
        num = (self.aZero(c) + n) % m
        return self.zeroA(num)

    def rotInts(self, n, m, l):
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


class TestRot(TestCase):
    def setUp(self):
        self.unit_under_test = Rot()


    def test_cIs3(self):
        self.assertEqual(3, self.unit_under_test.aZero('c'))


    def all_the_tests(self):
        if (aZero('c') != 2):
            print('expected aZero(\'c\') => 3 but it was ' + str(aZero('c')))
        if (aZero('z') != 25):
            print('expected aZero(z) => 26, but it was ' + str(aZero('z')))
        if (aZero('y') != 24):
            print('expected aZero(y) => 25, but it was ' + str(aZero('y')))
        if (zeroA(4) != 'E'):
            print('expected zeroA(4) => E, but it was ' + zeroA(4))
        if (zeroA(25) != 'Z'):
            print('expected zeroA(25) => Z, but it was ' + zeroA(26))
        if ((zeroA(aZero('z')) != 'Z')):
            print('expected zeroA(aZero(\'z\')) => Z, but it was ' + zeroA(aZero('z')))
        if (intsFromString('az') != [0, 25]):
            print('expected intsFromString(\'az\') => [0,25], but it was ' + intsFromString('az'))
        if (rotChar(13, 26, 'a') != 'N'):
            print('expected rotChar(13,26,\'a\') => \'N\', but it was ' + rotChar(13, 26, 'a'))
        if (rotChar(13, 26, 'n') != 'A'):
            print('expected rotChar(13,26,\'n\') => \'A\', but it was ' + rotChar(13, 26, 'n'))
        if (rotChar(1, 26, 'y') != 'Z'):
            print('expected rot(1, 26, \'y\') => Z, but it was ' + rotChar(1, 26, 'y'))
        if (rot(1, 26, string.ascii_lowercase) != 'BCDEFGHIJKLMNOPQRSTUVWXYZA'):
            print('expecting rot(1,26,ascii_lowercase) => \'BCDEFGHIJKLMNOPQRSTUVWXYZA\', ' +
                  'but it was ' + rot(1, 26, string.ascii_lowercase))
        if (rot(13, 26, string.ascii_lowercase) != 'NOPQRSTUVWXYZABCDEFGHIJKLM'):
            print('expecting rot(13,26,ascii_lowercase) => \'NOPQRSTUVWXYZABCDEFGHIJKLM\', ' +
                  'but it was ' + rot(13, 26, string.ascii_lowercase))
        if (applyKey('bbb', 'abc') != 'BCD'):
            print('expecting \'BCD\', but instead it was ' + applyKey('bbb', 'abc'))
        if (applyKey('b', 'ab') != 'BC'):
            print('expecting \'BC\' but instead it was ' + applyKey('b', 'ab'))
        if (applyKey('bc', 'bb') != 'CD'):
            print('expecting \'CD\' but instead it was ' + applyKey('bc', 'aa'))
