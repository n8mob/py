import sys

import requests


class CategoryMenu:
    def __init__(self, menu):
        self.categories_by_name = {}

        for name, category in menu['categories'].items():
            self.categories_by_name[name] = category['levels']

    @staticmethod
    def print(lines):
        for line in lines:
            print(line)


def choose_from_dict(choices, prompt):
    choice_menu = list(choices.keys())
    for i, choice_name in enumerate(choice_menu):
        print(f"{i}: {choice_name}")
    choice = input(prompt + ' ')
    if str.isnumeric(choice):
        return choices[choice_menu[int(choice)]]
    else:
        return choices[choice]

def choose_from_list(choices, prompt):
    for i, choice_name in enumerate(choices):
        print(f'\n{i}: {choice_name}')

    choice = input(prompt + ' ')
    return int(choice)


if __name__ == '__main__':
    url = 'https://puzzles.magiegame.com/menus/'
    response = requests.get(url)
    category_menu = CategoryMenu(response.json()[0])
    chosen_category = choose_from_dict(category_menu.categories_by_name, 'which category?')

    for level in chosen_category:
        for puzzle in level['puzzles']:
            print()
            CategoryMenu.print(puzzle['clue'])
            print()
            CategoryMenu.print(puzzle['init'])

            guessChar = sys.stdin.read(1)

            for i, winChar in enumerate(puzzle['winText']):
                while guessChar != winChar:
                    guessChar = sys.stdin.read(1)
                print(f'\r{puzzle["winText"][:i+1]}', end='')
                guessChar = ''

            print('\nCORRECT')
