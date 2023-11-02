import requests


class WebDictionary:
  def __init__(self, url='https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'):
    self.url = url
    self.by_length = {}

    response = requests.get(url)
    if not response.ok:
      print(response.text)
      return

    for word in response.text.split('\n'):
      word = word.strip().lower()

      wl = len(word)

      if wl not in self.by_length:
        print(f'first word of length {wl}: {word}')
        self.by_length[wl] = set()

      self.by_length[wl].add(word)


if __name__ == '__main__':
  d = WebDictionary()
  for word_length in d.by_length:
    count = len(d.by_length[word_length])
    print(f'{count} words of length {word_length}')
