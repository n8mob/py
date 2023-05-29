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


def choose_from_dict(choices):
    choice_menu = list(choices.keys())
    for i, choice_name in enumerate(choice_menu):
        print(f"{i}: {choice_name}")
    choice = input('which category? ')
    if str.isnumeric(choice):
        return choices[choice_menu[int(choice)]]
    else:
        return choices[choice]


def choose_index(choices):
    for i, choice in enumerate(choices):
        print(f"{i}: {choice}")

    choice = input('? ')
    return int(choice)


if __name__ == '__main__':
    url = 'https://puzzles.magiegame.com/menus/'
    response = requests.get(url)
    category_menu = CategoryMenu(response.json()[0])
    chosen_category = choose_from_dict(category_menu.categories_by_name)

    level_display_names = ['\n'.join(level['levelName']) for level in chosen_category]
    level_index = choose_index(level_display_names)
    print('\nlevel:\n' + level_display_names[level_index] + '\n')

    chosen_level = chosen_category[level_index]

    for puzzle in chosen_level['puzzles']:
        CategoryMenu.print(puzzle['clue'])
        guess = input('\n')
