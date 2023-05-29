import requests


class MAGiE:
  def __init__(self, menu):
    self.categories = {name: category for name, category in menu.items()}
      
    
  def print(self, lines):
    for line in lines:
      print(line)


if __name__ == '__main__':
  url = 'https://puzzles.magiegame.com/menus/'

  response = requests.get(url)
  menu = response.json()[0]

  magie = MAGiE(menu)
  
  for c in magie.categories:
    ['levels']:
    magie.print(level['levelName'])
