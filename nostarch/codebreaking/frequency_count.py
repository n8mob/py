import argparse
import sys


def main():
  pass


if __name__ == '__main__':
  """
  usage: frequency_count <filename>
  """
  #set up command-line arguments
  unparsed = argparse.ArgumentParser()
  unparsed.add_argument('filename')
  unparsed.add_argument('--case-sensitive', action='store_true')

  args = unparsed.parse_args()

  with open(args.filename, 'r') as f:
    text = f.read()

  counts = {}

  for c in text:
    if not args.case_sensitive:
      c = c.upper()
    if c not in counts:
      counts[c] = 0

    counts[c] += 1

  for c in range(ord('A'), ord('Z')+1):
    if chr(c) in counts:
      print(f'{chr(c)}: {counts.get(chr(c), 0)}')

  main()
