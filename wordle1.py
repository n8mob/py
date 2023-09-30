if __name__ == '__main__':
  before = input('before: ').upper()
  after = input('after: ').upper()

  nblank = 5 - (len(before) + len(after))

  remaining = input('remaining: ').upper()

  for i in range(len(remaining)):
    for j in range(nblank):
      for k in range(len(remaining)):
        print(before + remaining[i] + remaining[k] + after)
