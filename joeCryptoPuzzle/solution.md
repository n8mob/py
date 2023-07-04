HIIDOWNLOADEDACIPHERGENERATORJUSTFORFUN

HI I DOWNLOADED A CIPHER GENERATOR JUST FOR FUN

```python
import rot

with open('ciphertext.txt') as ctfile:
    ciphertext = ctfile.readline()
    if ciphertext[-1] == '\n':
        ciphertext = ciphertext[:-1]

rr = rot.Rot()

for i in range(26, 0, -1):
    candidate = rr.rot(i, 26, ciphertext)
    is_solution = input(f'does {candidate} look like a solution? y/N')
    if is_solution.lower() in ['', 'n']:
        continue
    else:
        print(f'\n{ciphertext} rotated by {i} is {candidate}!\n')
        break
    
```

