import xxhash
import hashlib

from pathlib import Path

if __name__ == '__main__':
  pics_path = Path('~/Pictures').expanduser()
  for item in pics_path.iterdir():
    print(item.name)
