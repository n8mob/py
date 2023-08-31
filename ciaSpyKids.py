punctuation = '.,'
etaoin_shrdlu = 'etaoinshrdlucmfwypvbgkjqxz'
guess_1 = 'teaoinshrdlucmfwypvbgkjqxz'
guess_2 = 'etaoinshrdlucmfwypvbgkjqxz'
guess_3 = 'aetoinshrdlucmfwypvbgkjqxz'
guess_4 = 'oetainshrdlucmfwypvbgkjqxz'

if __name__ == '__main__':
    original_cyphertext = """15 	3 	4 	9 	6 	16 	  	24 	20 	4 	19 	15 	  	24 	13 	4
    23 	24 	20, 	  	23 	17 	11 	  	16 	11 	4 	7 	13 	6 	22 	 
    3 	22 	11 	15 	  	13 	  	14 	9 	21 	17 	11 	4 	 
    7 	13 	14 	17 	9 	6 	11 	  	14 	13 	19 	19 	11 	15 	 
    23 	17 	11 	  	11 	6 	9 	16 	7 	13. 	  	9 	23 	 
    14 	20 	3 	19 	15 	  	22 	11 	6 	15 	  	13 	6 	15 	 
    4 	11 	14 	11 	9 	2 	11 	  	7 	11 	22 	22 	13 	16 	11 	22
    5 	3 	9 	14 	18 	19 	1 	  	13 	6 	15 	 
    22 	11 	14 	4 	11 	23 	19 	1"""

    despaced = original_cyphertext.split()

    include_punct = []
    ignoring_punct = []

    # assuming all punctuation follows a number
    for element in despaced:
        """assumptions:
         1. all punctuations follow the number
         2. each element contains at most 1 punctuation symbol"""
        if '.' in element or ',' in element:
            punct = '.' if '.' in element else ','
            index_of_punctuation = element.index(punct)
            ignoring_punct.append(element[:index_of_punctuation])
            include_punct.append(element[:index_of_punctuation])
            include_punct.append(element[index_of_punctuation:])
        else:
            include_punct.append(element)
            ignoring_punct.append(element)

    counts = {}

    for cc in ignoring_punct:
        if cc in counts:
            counts[cc] += 1
        else:
            counts[cc] = 1

    most_frequent = list(reversed(sorted(counts.items(), key=lambda count: count[1])))

    frequency_guess = list(etaoin_shrdlu)

    for i in range(len(etaoin_shrdlu)):
        new_guess = frequency_guess[i:] + frequency_guess[:i]

        frequency_guess = new_guess.copy()
        key_guess = {}

        for cc, frequency in most_frequent:
            key_guess[cc] = new_guess.pop(0)

        print(key_guess)

        attempted_solution = ''

        for cc in include_punct:
            if cc in key_guess:
                attempted_solution += key_guess[cc]
            else:
                attempted_solution += cc

        print(attempted_solution)
