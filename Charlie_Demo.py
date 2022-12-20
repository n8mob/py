
if __name__ == '__main__':
    person = "Unknown Person"
    while person != 'quit':
        person = input('What should I call you? ')
        print(f'Hello, {person}!')

    print(f'Goodbye, {person}.')
