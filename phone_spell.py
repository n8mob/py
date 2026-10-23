import sys


class PhoneSpell:
  LETTERS = {
    'A': '2',
    'B': '2',
    'C': '2',
    'D': '3',
    'E': '3',
    'F': '3',
    'G': '4',
    'H': '4',
    'I': '4',
    'J': '5',
    'K': '5',
    'L': '5',
    'M': '6',
    'N': '6',
    'O': '6',
    'P': '7',
    'Q': '7',
    'R': '7',
    'S': '7',
    'T': '8',
    'U': '8',
    'V': '8',
    'W': '9',
    'X': '9',
    'Y': '9',
    'Z': '9'
  }
  def spell(self, word):
    number = ''
    for letter in word.upper():
      number += self.LETTERS.get(letter, letter)
    return number


if __name__ == '__main__':
  ps = PhoneSpell()
  if len(sys.argv) > 1:
    ps.spell(sys.argv[1])
  else:
    word_to_spell = input('what should we spell? ')
    print(f'"{word_to_spell}" is spelled: "{ps.spell(word_to_spell)}"')