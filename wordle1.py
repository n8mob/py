before = input('before: ')
after = input('after: ')

nblank = 5 - (len(before) + len(after))

remaining = input('remaining: ').upper()

for i in range(len(nblank)):
  for j in range(len(nblank)):
    for c in remaining:
      print(before + c)

    
