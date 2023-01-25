import math

if __name__ == '__main__':
    person = "Unknown Person"
    while person != 'quit':
        if person == 'Thomas':
            number_of_digits = input(f'how many digits should I print?')
            print(f'{math.pi:number_of_digits}')
        else:
            person = input('What should I call you? ')
            print(f'Hello, {person}!')

    print(f'Goodbye, {person}.')
