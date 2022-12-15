full = sorted([4.58, 3.73, 3.76, 4.00, 5.17])
counted = full[1:-1]
assert len(counted) == len(full) - 2

print(sum(counted)/len(counted))

