from decimal import Decimal

one = Decimal(1)
four = Decimal(4)

if __name__ == '__main__':
  n = 1
  n = input('n? ')

  
  while str.isnumeric(n):
    n = int(n)
    pi = Decimal(3.0)
    
    is_neg = False
    
    for i in range(2, n, 2):
      id = Decimal(i)
      denom = id*id+1*id+2
      term = four/denom
      if is_neg:
        pi -= term
      else:
        pi += term
      
      is_neg = not is_neg
    
    print(f'π = {pi}')
    n = input('n? ')
