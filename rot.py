import string

def aZero(c):
    return ord(c.upper()) - ord('A')

def zeroA(n):
    return chr(n + ord('A'))

def stringFromInts(l, n=0):
    return ''.join(zeroA(c + n) for c in l)

def intsFromString(st, n=0):
    return [aZero(c) if c in string.ascii_letters else '' for c in st]

def rotChar(n, m, c):
    num = (aZero(c) + n) % m
    return zeroA(num)

def rotInts(n, m, l):
    return [(i + n) % m for i in l]

def rot(n, m, st):
    return ''.join(rotChar(n,m,c) for c in st)

def bruteRot(m, st):
    return [rot(n,m,st) for n in range(1,m)]

def applyKey(key, text, m=26):
    keyLen = len(key)
    txtLen = len(text)
    chunkSize = min(keyLen, txtLen)
    maxLen = max(keyLen, txtLen)
    return ''.join(
        rotChar(aZero(key[i]), m, text[i])
        for start in range(0,maxLen,chunkSize)
         for i in range(start,min(start+chunkSize,maxLen)))

if __name__ == '__main__':
    if (aZero('c') != 2):
        print ('expected aZero(\'c\') => 3 but it was ' + str(aZero('c')))
    if (aZero('z') != 25):
        print ('expected aZero(z) => 26, but it was ' + str(aZero('z')))
    if (aZero('y') != 24):
        print ('expected aZero(y) => 25, but it was ' + str(aZero('y')))
    if (zeroA(4) != 'E'):
        print ('expected zeroA(4) => E, but it was ' + zeroA(4))
    if (zeroA(25) != 'Z'):
        print ('expected zeroA(25) => Z, but it was ' + zeroA(26))
    if ((zeroA(aZero('z')) != 'Z')):
        print ('expected zeroA(aZero(\'z\')) => Z, but it was ' + zeroA(aZero('z')))
    if (intsFromString('az') != [0,25]):
        print ('expected intsFromString(\'az\') => [0,25], but it was ' + intsFromString('az'))
    if (rotChar(13,26,'a') != 'N'):
        print ('expected rotChar(13,26,\'a\') => \'N\', but it was ' + rotChar(13,26,'a'))
    if (rotChar(13,26,'n') != 'A'):
        print ('expected rotChar(13,26,\'n\') => \'A\', but it was ' + rotChar(13,26,'n'))
    if (rotChar(1, 26, 'y') != 'Z'):
        print ('expected rot(1, 26, \'y\') => Z, but it was ' + rotChar(1,26,'y'))
    if (rot(1,26,string.ascii_lowercase) != 'BCDEFGHIJKLMNOPQRSTUVWXYZA'):
        print ('expecting rot(1,26,ascii_lowercase) => \'BCDEFGHIJKLMNOPQRSTUVWXYZA\', ' +
               'but it was ' + rot(1,26,string.ascii_lowercase))
    if (rot(13,26,string.ascii_lowercase) != 'NOPQRSTUVWXYZABCDEFGHIJKLM'):
        print ('expecting rot(13,26,ascii_lowercase) => \'NOPQRSTUVWXYZABCDEFGHIJKLM\', ' +
               'but it was ' + rot(13,26,string.ascii_lowercase))
    if (applyKey('bbb', 'abc') != 'BCD'):
        print('expecting \'BCD\', but instead it was ' + applyKey('bbb', 'abc'))
    if (applyKey('b', 'ab') != 'BC'):
        print('expecting \'BC\' but instead it was ' + applyKey('b', 'ab'))
    if (applyKey('bc', 'bb') != 'CD'):
        print('expecting \'CD\' but instead it was ' + applyKey('bc', 'aa'))
