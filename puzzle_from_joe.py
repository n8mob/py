"""@mrGrigg sent me this puzzle long ago

IJJEPXOMPBEFEBDJQIFSHFOFSBUPSKVTUGPSGVO

I failed to solve it back then.
Not sure why, it wasn't too hard.
I think he was surprised that I couldn't solve it.
Now that I /have/ solved it, I'm a bit surprised as well.
"""
import rot

def find_ijj(ciphertext):
  ciphertext = ciphertext.strip()
  interactive_brute(ciphertext)


def interactive_brute(ciphertext):
  rr = rot.Rot()

  for i in range(1, 26):
    candidate = rr.rot_string(i, 26, ciphertext)
    is_solution = input(f'does {candidate} look like a solution? y/N ')
    if is_solution.lower() in ['', 'n']:
      continue
    else:
      print(f'\n{ciphertext} rotated by {i} is {candidate}!\n')
      break


if __name__ == '__main__':
  interactive_brute('IJJEPXOMPBEFEBDJQIFSHFOFSBUPSKVTUGPSGVO')
