from math import floor
import random
import ui
import logging


class DiceRoller:

  def __init__(
    self,
    view: ui.View,
    no_dice=5,
    dice_size=55,
    dice_center_y=120
    ):
    self.log = logging.getLogger("dice_game")
    self.no_dice = no_dice

    self.view = view

    self.width = view.frame.size.x
    self.height = view.frame.size.y
    self.dice_size = dice_size
    self.dice_center_y = dice_center_y
    self.dice_color = '#009292'
    self.hold_color = '#7106db'

    self.dice = []
    self.init_dice()
    self.roll_button = self.init_roll_button()

  def init_dice(self):
    dice_space = self.view.frame.size.x // self.no_dice
    die_margin = dice_space // 4
    for i in range(self.no_dice):
      button = ui.Button()
      button.num = random.randint(1, 6)
      button.title = str(button.num)
      button.hold = False

      die_x = (i * dice_space) + die_margin
      button.center = (die_x, self.dice_center_y)
      button.width = self.dice_size
      button.height = self.dice_size
      button.border_color = self.dice_color
      button.border_width = 1
      button.action = self.dice_click
      button.index = i

      self.view.add_subview(button)
      self.dice.append(button)

  def dice_click(self, sender):
    if not sender.hold:
      sender.hold = True
      sender.border_color = '#7106db'
      sender.border_width = 3
    else:
      sender.hold = False
      sender.border_color = 'teal'
      sender.border_width = 1

  def init_roll_button(self):
    roll_button = ui.Button()
    roll_button.center = (self.dice_size * 3, self.dice_center_y * 2)
    roll_button.title = 'Roll'
    roll_button.width = 80
    roll_button.height = self.dice_size
    roll_button.border_color = 'teal'
    roll_button.border_width = 2
    roll_button.action = self.roll
    self.view.add_subview(roll_button)
    return roll_button

  def roll(self, sender):
    if not self.dice:
      self.log.error('no dice, son')
      return
    else:
      for die in self.dice:
        if not die.hold:
          num = random.randint(1, 6)
          die.num = num
          die.title = str(num)


if __name__ == '__main__':
  v = ui.load_view()
  v.width = ui.get_window_size().x
  v.height = ui.get_window_size().y
  v.flex = 'WH'
  dice = DiceRoller(v)

  v.present('sheet')

