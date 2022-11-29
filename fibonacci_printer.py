last = 0
current = 1

while(True):
  nowone = last + current
  print(nowone)
  last = current
  current = nowone
