import time
i = 1

start = time.perf_counter()

while i < 10_000_000:
  if i % 100_000 == 0:
    lapTime = time.perf_counter() - start
    print(f'{lapTime:.9} seconds to {i:,}')
  i = i + 1
  
end = time.perf_counter()
elapsed = end - start
  
print(f'{elapsed:.9} seconds from 1 to {i:,}')
