from math import floor
import random
import ui

d = []
v = ui.load_view()
v.flex = 'WH'
no_dice = 5  # as in "No. of dice"
dice_center_y = 50
dice_space = floor(
  ui.get_window_size().x // no_dice
  )
half_die = dice_space // 4
dice_size = floor(dice_space * 0.6)

def init_dice():
  for i in range(0, no_dice):
    button = ui.Button()
    d.append(button)
    
    button.num = random.randint(1,6)
    button.title = str(button.num)
    button.hold = False

    die_x = (i * dice_space) + half_die
    button.center = (die_x, dice_center_y)
    button.width = dice_size
    button.height = dice_size
    button.border_color = 'teal'
    button.border_width = 1
    button.action = dice_click
    button.index = i
    v.add_subview(button)
    
def dice_click(sender):
  if not sender.hold:
    sender.hold = True
    sender.border_color = '#7106db'
    sender.border_width = 3
  else:
    sender.hold = False
    sender.border_color = 'teal'
    sender.border_width = 1
  
def roll(sender):
  for i in range(len(d)):
    if not d[i].hold:
      num = random.randint(1,6)
      d[i].num = num
      d[i].title = str(num)
    
roll_button = ui.Button()
roll_button.center = (dice_size * 3, dice_center_y * 3)
roll_button.title = 'Roll'
roll_button.width = 80
roll_button.height = dice_size
roll_button.border_color = 'teal'
roll_button.border_width = 2
roll_button.action = roll
v.add_subview(roll_button)

init_dice()
v.present('sheet')


