import math
import re
import sys

from web_words import WebDictionary

def brute_force_center(dictionary):
  before = input('before: ').lower()
  after = input('after: ').lower()
  nblank = 5 - (len(before) + len(after))
  remaining = input('remaining: ').lower()
  for i in range(len(remaining)):
    for j in range(nblank):
      for k in range(len(remaining)):
        guess = before + remaining[i] + remaining[k] + after
        if guess in dictionary:
          print(guess.upper())

def words_by_regex(set_dictionary):
  dictionary = sorted(set_dictionary)
  
  pattern = input('regex: ')
  
  regex = re.compile(f'^{pattern}$')
  
  for word in dictionary:
    if regex.match(word):
      print(word)
      
  print('end')
  

def all_with_prefix(set_dictionary):
  dictionary = sorted(set_dictionary)
  prefix = input('before: ').lower()
  prefix_len = len(prefix)
  letter_scale = math.floor(len(dictionary) / 26)

  prefix_letter_index = ord(prefix[0]) - ord('`') #  last char before 'a' is '`'
  assert 0 < prefix_letter_index < 27, f'Unexpected letter index: {prefix_letter_index}'

  start_index = math.floor(prefix_letter_index * letter_scale)
  assert type(start_index) != float, 'I thought math.floor would return an integer'

  search_index = start_index
  scale_step = letter_scale

  while dictionary[search_index][:prefix_len] != prefix:
    guess = dictionary[search_index]
    print(f'guess: {guess}')
    guess_check = guess[:prefix_len]
    if guess_check > prefix:
      print('started too high')
      print(guess)
      print('scaling by ' + str(scale_step))
      search_index -= scale_step
    elif guess_check < prefix:
      print('started too low')
      print(guess)
      print('scaling by ' + str(scale_step))
      search_index += scale_step
    else:
      print(f'is {guess} correct?')

    scale_step = math.floor(scale_step / 2)

  suffix = input('after: ').lower()
  
  guess = dictionary[search_index]

  while guess[:prefix_len] == prefix:
    print(f'is it {guess}?')
    search_index += 1
    guess = dictionary[search_index]


if __name__ == '__main__':
  web_dict = WebDictionary()
  d = web_dict.by_length[5]

  words_by_regex(d)
  sys.exit(0)
  
