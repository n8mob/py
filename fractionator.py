import fractions
prompt = 'n: '


def main():
  s = input(prompt)
  debug = False
  if s.lower().startswith('debug'):
    debug = True
    print('debug mode')
    s = input(prompt)
  while not s.lower().startswith('quit'):
    n = float(s)
    if debug:
      print(f's: {s}\tn: {n}')

    fraction = fractions.Fraction.from_float(n).limit_denominator(9999)
    print(fraction)

    s = input(prompt)

  print('goodbye')


if __name__ == '__main__':
    main()
