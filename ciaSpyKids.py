punctuation = '.,'
etaoin_shrdlu = 'etaoinshrdlucmfwypvbgkjqxz'
guess_1 = 'teaoinshrdlucmfwypvbgkjqxz'
guess_2 = 'etaoinshrdlucmfwypvbgkjqxz'
guess_3 = 'aetoinshrdlucmfwypvbgkjqxz'
guess_4 = 'oetainshrdlucmfwypvbgkjqxz'
vowels_first = 'eaioutnshrdlcmfwypvbgkjqxz'
modified = 'stdoanirelcmguywpvbfkjqxz'


def count_original():
    original_cyphertext = """
15  3  4  9  6  16
24  20  4  19  15
24  13  4
23  24  20,
23  17  11
16  11  4  7  13  6  22   
3  22  11  15
13
14  9  21  17  11  4   
7  13  14  17  9  6  11
14  13  19  19  11  15
23  17  11
11  6  9  16  7  13.
9  23
14  20  3  19  15
22  11  6  15
13  6  15
4  11  14  11  9  2  11
7  11  22  22  13  16  11  22
5  3  9  14  18  19  1
13  6  15
22  11  14  4  11  23  19  1"""
    de_spaced = original_cyphertext.split()
    with_punct = []
    without_punct = []
    # assuming all punctuation follows a number
    for element in de_spaced:
        """assumptions:
         1. all punctuations follow the number
         2. each element contains at most 1 punctuation symbol"""
        if '.' in element or ',' in element:
            punct = '.' if '.' in element else ','
            index_of_punctuation = element.index(punct)
            without_punct.append(element[:index_of_punctuation])
            with_punct.append(element[:index_of_punctuation])
            with_punct.append(element[index_of_punctuation:])
        else:
            with_punct.append(element)
            without_punct.append(element)
    counts = {}
    for cc in without_punct:
        if cc in counts:
            counts[cc] += 1
        else:
            counts[cc] = 1

    by_frequency = list(reversed(sorted(counts.items(), key=lambda count: count[1])))
    return with_punct, by_frequency


def brute_1(with_punct, by_frequency ):

    frequency_guess = list(vowels_first)

    for i in range(26):
        new_guess = frequency_guess[i:] + frequency_guess[:i]

        try_guess(new_guess, with_punct, by_frequency)


def try_guess(guess, with_punct, by_frequency):
    frequency_guess = guess.copy()
    key_guess = {}
    for cc, frequency in by_frequency:
        key_guess[cc] = frequency_guess.pop(0)

    print(key_guess)
    attempted_solution = ''
    for cc in with_punct:
        if cc in key_guess:
            attempted_solution += key_guess[cc]
        else:
            attempted_solution += cc
    print(attempted_solution)


def enter_key(with_punct, by_frequency):
    while True:
        key_guess = input('key guess: ')
        try_guess(list(key_guess), with_punct, by_frequency)


if __name__ == '__main__':
    include_punct, most_frequent = count_original()
    enter_key(include_punct, most_frequent)

