import random

def is_good(can):
  return (
    '  ' not in can and
    not can[0] == ' ' and
    not can[-1] == ' '
    )

def main():
  orig = input('type scrambled: ')
  working = list(orig)
  
  i = 0
    
  while i < 20:
    random.shuffle(working)
    can = ''.join(working)
    if is_good(can):
      i+=1
      print(can)
    else:
      continue
    
    
if __name__ == '__main__':
  main()
