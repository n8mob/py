import unicodedata


def encode(phrase: str):
    phrase_nums = ':'.join([f'{ord(b):X}' for b in phrase])
    print(phrase_nums)

    for letter in phrase:
        print_details_for(letter)


def print_details_for(letter):
    n = ord(letter)
    print(f'{letter}: dec: {n} hex: {n:x} subd: {n - 64} bin: {n:08b}')


def print_unicode_for(letter):
    name_for_letter = unicodedata.name(letter)
    print(f'the name of {ord(letter)} is {name_for_letter}')


def make_ascii_table():
    pass


if __name__ == '__main__':
    print_unicode_for(chr(160))
    # encode('UPSTAIRS BOOKSHELF')
