#!/usr/bin/python
from tabulate import tabulate


def to_base(n, base):
    if n == 0:
        return [0]

    digits = []
    while n:
        digits.append(int(n % base))
        n //= base

    return digits[::-1]


def string_in_base(n, base):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7',
              '8', '9', 'A', 'B', 'C', 'D', 'E', 'F',
              'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
              'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V']
    return ''.join(digits[d] for d in to_base(n, base))


if __name__ == '__main__':
    bases = [10, 32, 16, 8, 4, 2]
    base_heads = ['Decimal', 'Base 32', 'Hexadecimal', 'Octal', 'Base 4', 'Binary']

    top = int(input('enter top number: ')) + 1

    representations = []

    for n in range(top):
        representations.append([string_in_base(n, b) for b in bases])

    with open('big_basis.txt', 'w') as outfile:
        outfile.write(tabulate(representations, headers=base_heads, tablefmt='orgtbl'))
