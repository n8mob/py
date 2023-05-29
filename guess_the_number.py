import random

def guess_the_number(low=0, high=10):
  the_number = random.randint(low,high+1)
  tries = 0
  guess = -1
  
  while guess != the_number:
    guess = ask_for_a_guess()
    if guess < the_number:
      too_low()
    elif guess > the_number:
      too_high()
    else:
      that_is_correct()


def ask_for_a_guess():
  guess = input('what is your guess? ')
  return int(guess)
  

def too_low():
  print('that is too low; please guess again ')
  
  
def too_high():
  print('that is too high; please guess again ')
  
  
def that_is_correct():
  print('that is too right!')
  
  
guess_the_number()
