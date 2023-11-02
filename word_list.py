class SystemDictionary:
  def __init__(self):
    self.base_path = '/usr/share/dict/'
    self.by_length = {}
    self.by_first_letter = {}
    self.proper_names = set()
    # noinspection SpellCheckingInspection
    with open(self.base_path + 'propernames') as proper_names_file:
      for name in proper_names_file.read().split('\n'):
        if name:
          self.proper_names.add(name)

    with open(self.base_path + 'words') as word_list:
      for word in word_list.read().split('\n'):
        if not word or word in self.proper_names:
          continue
        assert not word[-1] == '\n'

        word = word.lower()

        wl = len(word)
        if wl not in self.by_length:
          print(f'first word of length {wl}: {word}')
          self.by_length[wl] = set()

        self.by_length[wl].add(word)

        first_letter = word[0]
        if first_letter not in self.by_first_letter:
          print(f'first word starting with {first_letter}: {word}')
          self.by_first_letter[first_letter] = []

        self.by_first_letter[first_letter].append(word)


if __name__ == '__main__':
  d = SystemDictionary()
  for word_length in d.by_length:
    count = len(d.by_length[word_length])
    print(f'{count} words of length {word_length}')

  for letter in d.by_first_letter:
    count = len(d.by_first_letter[letter])
    print(f'{letter}: {count} words')
