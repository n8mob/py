import sys
import curses
import time

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


def try_a_puzzle():
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

            guessPhrase = None
            guessChar = None
            win_index = 0
            winChar = puzzle['winText'][win_index]

            while guessPhrase != puzzle['winText']:
                guessChar = getch()
                if guessChar == winChar:
                    print(puzzle['winText'][:win_index])
                else:
                    print('\b')

            print('\nCORRECT')


def guess_loop(scr: curses.window):
    curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    incorrect = curses.color_pair(1) | curses.A_BOLD
    correct = curses.color_pair(2) | curses.A_BOLD

    win_message = 'test'
    guess_message = ''
    i = 0
    guess_char = 'X'

    while guess_message != win_message:
        scr.refresh()
        if guess_char == win_message[i]:
            i += 1
            guess_message += guess_char

            scr.addstr(2, 2, guess_message, correct)
        else:
            scr.addstr(2, 2, guess_message, correct)
            scr.addstr(guess_char, incorrect)

        guess_char = chr(scr.getch())

    a = True

    for blinkquit in range(12):
        time.sleep(0.6)
        color = correct if a else incorrect
        a = not a
        scr.clear()
        scr.addstr(2, 2, 'CORRECT', color)
        scr.refresh()

if __name__ == '__main__':
    curses.wrapper(guess_loop)
