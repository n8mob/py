import random
import datetime as dt
from old_rot import rot, bruteRot

def is_good(can, found_sofar):
  return (
    '  ' not in can and
    not can[0] == ' ' and
    not can[-1] == ' ' and
    can not in found_sofar
    )

def main():
  orig = input('type scrambled: \n')
  print()
  working = list(orig)
  
  i = 0
  found_sofar = []
    
  while i < 50:
    random.shuffle(working)
    can = ''.join(working)
    if is_good(can, found_sofar):
      i+=1
      found_sofar.append(can)
      print(can)
    else:
      continue
    
    
if __name__ == '__main__':
  caldate = dt.datetime(2022,8,24)
  since = dt.datetime.today() - caldate

  print(f'{since.days} days since {caldate}')
