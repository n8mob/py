import random
from num2words import num2words

my_values = [
    'creativity',
    'love',
    'discovery',
    'freedom',
    'honesty',
    'humor',
    'mastery',
    'beauty',
    'humility',
    'self confidence',
    'precision',
    'power',
    'integrity',
]

my_value_counts = {}

for value in my_values:
    my_value_counts[value] = 0

if __name__ == '__main__':
    keep_going = input("Shall we? ")
    print("('Q' to quit)")

    while keep_going:
        pair = random.choice(my_values), random.choice(my_values)
        while pair[0] == pair[1]:
            pair = random.choice(my_values), random.choice(my_values)

        choice_number_string = input(f'1: {pair[0]} or 2: {pair[1]}? ')
        if choice_number_string.upper() == 'Q':
            keep_going = None
            break
        else:
            choice_number = int(choice_number_string) - 1
            choice = pair[choice_number]
            my_value_counts[choice] += 1
            nth = num2words(my_value_counts[choice], to='ordinal')

    for value, count in my_value_counts.items():
        print(f'{value}: {count} time{"" if count == 1 else "s"}')
