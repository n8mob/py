prompt = 'n: '
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
  print(float.as_integer_ratio(n))
  s = input(prompt)

print('goodbye')
