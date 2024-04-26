#!/usr/bin/env python3
import os
import shutil
import sys
import logging


if __name__ == '__main__':
  log = logging.getLogger()
  file_list_path = sys.argv[1]
  copy_dest_dir = sys.argv[2]
  move_dest_dir = sys.argv[3]

  with open(file_list_path, 'r') as f:
    file_list = [l.strip() for l in f.read().splitlines()]

  print(f'read {file_list_path}')
  print('which starts with:')
  for file_name in file_list[0:5]:
    print(file_name)

  if os.path.exists(copy_dest_dir):
    print(f'prepared to copy to {copy_dest_dir}')
  else:
    print(f'copy destination ({copy_dest_dir}) does not exist')

  if os.path.exists(move_dest_dir):
    print(f'prepared to move to {move_dest_dir}')
  else:
    print(f'move destination ({move_dest_dir}) does not exist')

  file_count = len(file_list)

  for i, file_path in enumerate(file_list):
    file_path = file_path.strip()
    if not file_path:
      continue
    if not os.path.exists(file_path):
      log.error(f'file {i:02}/{file_count}\t{file_path}\t\tdoes not exist')
      continue

    print(f'{i:02}/{file_count}\t{file_path}\t', end='', flush=True)
    shutil.copy2(file_path, copy_dest_dir)
    print('copied\t', end='', flush=True)
    shutil.move(file_path, move_dest_dir)
    print('moved\t', flush=True)
