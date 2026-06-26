import xxhash
import hashlib

import time

from pathlib import Path

NS_PER_MS = 1_000_000
ANOMALY_THRESHOLD_20_PERCENT = 0.2
"""75 MB"""
FILE_SIZE_LIMIT = 75_000_000
B_PER_MB = 1_000_000

def walk_directory(operator):
  pics_path = Path(directory_name).expanduser()
  dirs = []
  outlier_times_ms = []

  start_time_ns = time.perf_counter_ns()
  item_count = 0
  subset_limit = 10_000
  total_elapsed_ns = 0
  reporting_threshold_ms = 15
  running_avg_ms = 0

  for item in pics_path.iterdir():
    if item.is_dir():
      dirs.append(item.name)
    else:
      if item.stat().st_size > FILE_SIZE_LIMIT:
        print_red(f'ignoring {item.name} because it is too large ({item.stat().st_size/B_PER_MB} MB)')
        continue
      item_count += 1
      item_start_ns = time.perf_counter_ns()
      operator.operate(item)
      item_elapsed_ms = (time.perf_counter_ns() - item_start_ns) / NS_PER_MS
      if item_elapsed_ms > reporting_threshold_ms:
        outlier_times_ms.append([item.name,item_elapsed_ms])
      total_elapsed_ns += item_elapsed_ms
      running_avg_ms = total_elapsed_ns / item_count / NS_PER_MS
      if running_avg_ms > reporting_threshold_ms:
        reporting_threshold_ms = running_avg_ms * ANOMALY_THRESHOLD_20_PERCENT
        print_red(f'Updating reporting threshold to {reporting_threshold_ms} ms')
    if item_count >= subset_limit:
      print_red(f'stopping after limit of {item_count} items')
      break

  print(f'operated on {pics_path.name} directory with `{type(operator).__name__}`\n')

  elapsed_ms = (time.perf_counter_ns() - start_time_ns) / NS_PER_MS
  print_blue(f'total elapsed time: {elapsed_ms} ms')
  print(f'item count: {item_count}')
  print_blue(f'avg time: {elapsed_ms / item_count} ms')

  if dirs:
    print_green(f'{len(dirs)} directories:')
    for dir_name in dirs:
      print_green(dir_name)

  if outlier_times_ms:
    print_red(f'{len(outlier_times_ms)} outliers:')
    for item_name, item_elapsed_ms in outlier_times_ms:
      print_red(f'{item_name}:\t\t{item_elapsed_ms} ms')

class SimplePrinter:
  @staticmethod
  def operate(item):
    print(f'operating on {item.name}')


class HasherMD5:
  def __init__(self):
    self.md5_hash = hashlib.md5()

  def operate(self, item):
    with open(item, 'rb') as file:
      for chunk in iter(lambda: file.read(4096), b''):
        self.md5_hash.update(chunk)

    print(f'{item.name}:\t\t{self.md5_hash.hexdigest()}')


class HasherXXHash:
  def __init__(self):
    self.xxhash_hash = xxhash.xxh64()

  def operate(self, item):
    print(f'{item.name}:', end='\t\t')
    with open(item, 'rb') as file:
      for chunk in iter(lambda: file.read(4096), b''):
        self.xxhash_hash.update(chunk)

    print(f'{self.xxhash_hash.hexdigest()}')


def print_red(s: str):
  print(f'\n\033[91m{s}\033[0m')


def print_green(s: str):
  print(f'\033[92m{s}\033[0m')


def print_blue(s: str):
  print(f'\033[94m{s}\033[0m')


if __name__ == '__main__':
  directory_name = '~/Pictures'
  op = HasherMD5()
  # op = HasherXXHash()
  # op = SimplePrinter()

  walk_directory(op)
