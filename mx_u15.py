def print_by_n(s: str, n):
  s = s.strip()
  i = 0
  while i < len(s):
    chunk = ''.join('⬜' if c == '1' else '⬛' for c in s[i:i + n])
    print(chunk)
    i += n


def the_puzzle(bitwidth=80):
  """I had forgotten where this came from

  It seems that it was probably on a billboard for MX.com on I15 near the Point of The Mountain

  Suspecting a bit-map image, I wrote a loop to try chopping the string up into different line lengths
  '1' and '0' don't have enough visual contrast for the image to show up,
  so I replaced them with white and black square emojis in the print_by_n function above.

  I did check the string length: 913.
  Turns out, that is the product of two primes, 11 and 83.

  The message appeared when my trial and error loop reached 83.

  After seeing the image (which happens to be text), my son noticed that he could read it
  in the 82-wide image.

  We looked at the 84-wide image and it was pretty visible, but the first characters wrapped around to the back.

  I originally started the bitwidth variable at 23
  I have left it initialized to 80 in case you want the fun of running a few iterations
  and seeing the message appear
  """
  bigString = '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000011010000100010000000000001111000011110001101000000001000011110001111100010000100000101010000101000000000000100000001000010010101000000100001000000010000100100001000001010100000100000000000001000000010000100101010000010000010000000100001001000010000010101000010100000110000010000000100001001010100001000000100000001000010010001100000100010001000100001100000011110000111100010001000100000000111100011111000011101000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
  stringlength = len(bigString)
  print(f'bitstring length: {stringlength}')

  should_continue = True
  while should_continue:
    print_by_n(bigString, bitwidth)
    bitwidth += 1
    should_continue = input(f'continue with width {bitwidth}? [y/n] ').lower() == 'y'


if __name__ == '__main__':
  the_puzzle()

