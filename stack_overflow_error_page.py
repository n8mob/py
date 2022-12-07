"""The error page on stackoverflow.com had an image with a bunch of control codes in it.
I want to see if the control codes have some Easter egg in them.

So far I have only isolated the control codes. I have not even looked for an Easter egg yet."""

from curses import ascii

ascii_hex_table = '''
     00 nul   01 soh   02 stx   03 etx   04 eot   05 enq   06 ack   07 bel
     08 bs    09 ht    0a nl    0b vt    0c np    0d cr    0e so    0f si
     10 dle   11 dc1   12 dc2   13 dc3   14 dc4   15 nak   16 syn   17 etb
     18 can   19 em    1a sub   1b esc   1c fs    1d gs    1e rs    1f us
     20 sp    21  !    22  "    23  #    24  $    25  %    26  &    27  '
     28  (    29  )    2a  *    2b  +    2c  ,    2d  -    2e  .    2f  /
     30  0    31  1    32  2    33  3    34  4    35  5    36  6    37  7
     38  8    39  9    3a  :    3b  ;    3c  <    3d  =    3e  >    3f  ?
     40  @    41  A    42  B    43  C    44  D    45  E    46  F    47  G
     48  H    49  I    4a  J    4b  K    4c  L    4d  M    4e  N    4f  O
     50  P    51  Q    52  R    53  S    54  T    55  U    56  V    57  W
     58  X    59  Y    5a  Z    5b  [    5c  \\   5d  ]    5e  ^    5f  _
     60  `    61  a    62  b    63  c    64  d    65  e    66  f    67  g
     68  h    69  i    6a  j    6b  k    6c  l    6d  m    6e  n    6f  o
     70  p    71  q    72  r    73  s    74  t    75  u    76  v    77  w
     78  x    79  y    7a  z    7b  {    7c  |    7d  }    7e  ~    7f del
     '''


oca_from_mac = '''
^@^C^A>^D^A^@^P^@^C^AL^D^A^@^T^@^C^A°
- stack overflow^M
^@^C^@R6003^M
- integer divide by 0^M
^@      ^R6009^M
- not enough space for environment^M
^@^R^@R6018^M
- unexpected heap error^M
^@ü^@^M
^@ÿ^@run-time error ^@^B^@R6002^M
- floating-point support not loaded^M
'''


def get_control_chars(s):
    for oi in range(len(s)-1):
        if s[oi] == '^':
            yield s[oi:oi+2]


if __name__ == '__main__':
    console_control_chars = [cc for cc in get_control_chars(oca_from_mac)]
    stripped_control_codes = [cc[-1] for cc in console_control_chars]
    decoded_raw_chars = [ord(cc) - ord('@') for cc in stripped_control_codes]
    re_encoded = [chr(c) for c in decoded_raw_chars]

    if len(console_control_chars) != len(decoded_raw_chars):
        print(f'Oops, {len(console_control_chars)=} and {len(decoded_raw_chars)=}')

    print(f'^C\tC\t0\tname')
    for ci in range(len(re_encoded)):
        name = ascii.controlnames[decoded_raw_chars[ci]]
        print(f'{console_control_chars[ci]}\t{decoded_raw_chars[ci]}\t{name}')

    byte_array = bytes(decoded_raw_chars)

