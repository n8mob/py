punctuation = '.,'
etaoin_shrdlu = 'etaoinshrdlucmfwypvbgkjqxz'
guess_1 = 'teaoinshrdlucmfwypvbgkjqxz'
guess_2 = 'etaoinshrdlucmfwypvbgkjqxz'
guess_3 = 'aetoinshrdlucmfwypvbgkjqxz'
guess_4 = 'oetainshrdlucmfwypvbgkjqxz'
vowels_first = 'eaioutnshrdlcmfwypvbgkjqxz'
modified = {
    'stdoainrelcgmuywpvbfkjqxz': 'duringywredytrlywlcsgsrmtnouosdtaivcsrmtacinsateesdlcssnigmtilawuedosndtndrsasiksmsootgsofuiabeptndosarslep',
}


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
    lines = original_cyphertext.split('\n')
    lines_with_punctuation = {'.': [], ',': []}
    for line_number, line in enumerate(lines):
        line = line.replace(' \t', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('\n', '')

        for punct in lines_with_punctuation:
            if punct in line:
                lines_with_punctuation[punct].append(line_number)
                line = line.replace(punct, '')
        lines[line_number] = line

    raw_cypher = []

    for line in lines:
        for char in line.split(' '):
            if char == '':
                continue
            raw_cypher.append(char)

    print(raw_cypher)

    counts = {str(c): 0 for c in range(1, 26)}
    for cc in raw_cypher:
        counts[cc] += 1

    by_frequency = list(reversed(sorted(counts.items(), key=lambda count: count[1])))
    return raw_cypher, by_frequency


def brute_1(with_punct, by_frequency):
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


def enter_key(raw_cypher, by_frequency):
    while True:
        key_guess = input('key guess: ')
        try_guess(list(key_guess), raw_cypher, by_frequency)


if __name__ == '__main__':
    _raw_cypher, _most_frequent = count_original()
    enter_key(_raw_cypher, _most_frequent)
