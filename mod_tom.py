from math import modf

cmd = '50'
while cmd != 'q':
  n = int(cmd)
  print(f'{n} mod 26 is {n%26}')
  cmd = input('what to mod by 26? ')
  
print("done modding.\nlet's count letters!")

cmd = 'a'
while cmd != 'quit now':
  n = ord(cmd)
  print(f"ord({cmd}) = {n}")
  cmd = input('letter, please: ')
print('goodbye\ngoodbye')

print([ord(c) for c in 'HELLO'])
