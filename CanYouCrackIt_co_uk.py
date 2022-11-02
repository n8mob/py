from unittest import TestCase


class TestRound1(TestCase):
    def setUp(self) -> None:
        self.raw_string = """
            eb 04 af c2 bf a3 81 ec   00 01 00 00 31 c9 88 0c
            0c fe c1 75 f9 31 c0 ba   ef be ad de 02 04 0c 00
            d0 c1 ca 08 8a 1c 0c 8a   3c 04 88 1c 04 88 3c 0c
            fe c1 75 e8 e9 5c 00 00   00 89 e3 81 c3 04 00 00
            00 5c 58 3d 41 41 41 41   75 43 58 3d 42 42 42 42
            75 3b 5a 89 d1 89 e6 89   df 29 cf f3 a4 89 de 89
            d1 89 df 29 cf 31 c0 31   db 31 d2 fe c0 02 1c 06
            8a 14 06 8a 34 1e 88 34   06 88 14 1e 00 f2 30 f6
            8a 1c 16 8a 17 30 da 88   17 47 49 75 de 31 db 89
            d8 fe c0 cd 80 90 90 e8   9d ff ff ff 41 41 41 41
"""
        self.stripped = self.raw_string.replace(' ', '')
        self.stripped = self.stripped.replace('\n', '')
        self.stripped = self.stripped.replace('\r', '')

        self.byte_array = bytearray.fromhex(self.stripped)

        self.expected_byte_count = 160

    def test_strip_spaces(self):
        _stripped = self.raw_string.replace(' ', '')
        _stripped = _stripped.replace('\n', '')
        _stripped = _stripped.replace('\r', '')

        actual = bytearray.fromhex(_stripped)
        expected_not = b' '

        self.assertFalse(expected_not in actual, f'expecting no space characters ({expected_not})')

        self.assertEqual(self.expected_byte_count, len(actual), 'length of local array')
        self.assertEqual(self.expected_byte_count, len(self.byte_array), 'length of self.byte_array')

    def test_without_stripping(self):
        actual = bytearray.fromhex(self.raw_string)

        self.assertEqual(self.byte_array, actual)

    def test_count_bytes(self):
        counts = {}

        for b in self.byte_array:
            if b in counts:
                counts[b] += 1
            else:
                counts[b] = 1

        for b in counts:
            print(f'{hex(b)}:\t{counts[b]}')

        self.assertEqual(self.expected_byte_count, len(self.byte_array))

        self.assertTrue(len(counts) < self.expected_byte_count, 'Duplicates should make the length of uniques less than the length of the whole array')

    def test_even_odd(self):
        bits = []
        for b in self.byte_array:
            bits.append(str(b % 2))

        bitstrings = []
        concatenated_bytes = bytearray()

        for i in range(0, len(bits), 8):
            bitstrings.append(''.join(bits[i:i+8]))

        print(bitstrings)

        for bs in bitstrings:
            concatenated_bytes.append(int(''.join(bs), 2))

        print(concatenated_bytes.decode())
