def encode(phrase: str):
    phrase_nums = ':'.join([f'{ord(b):X}' for b in phrase])
    print(phrase_nums)

    for letter in phrase:
        numeric_letter = ord(letter)
        print(f'{letter}: dec: {numeric_letter} hex: {numeric_letter:x} subd: {numeric_letter-64} bin: {numeric_letter:08b}')


def make_ascii_table():
    pass


if __name__ == '__main__':
    encode('UPSTAIRS BOOKSHELF')
    
