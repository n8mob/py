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
    num = random.randint(1,6)
    d.append([button, num])
    button.title = str(num)
    die_x = (i * dice_space) + half_die
    button.center = (die_x, dice_center_y)
    button.width = dice_size
    button.height = dice_size
    button.border_color = 'teal'
    button.border_width = 1
    v.add_subview(button)
  
def roll(sender):
  for i in range(len(d)):
    num = random.randint(1,6)
    d[i][0].title = str(num)
    
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


