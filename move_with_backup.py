#!/usr/bin/env python3
import os
import shutil
import sys




def move_with_backup(src_file_path, copy_dest_dir, move_dest_dir):
  shutil.copy2(src_file_path, copy_dest_dir)
  shutil.move(src_file_path, move_dest_dir)

if __name__ == '__main__':
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

  for file_name in file_list:
    move_with_backup(file_name, copy_dest_dir, move_dest_dir)
