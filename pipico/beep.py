import time
import board
import digitalio
import pwmio
from digitalio import DigitalInOut
from pwmio import PWMOut

DAH = 'DAH'

DIT = 'DIT'

MORSE = {
  (DIT,): 'E',
  (DAH,): 'T',
  (DIT, DIT): 'I',
  (DIT, DAH): 'A',
  (DAH, DIT): 'N',
  (DAH, DAH): 'M',
  (DIT, DIT, DIT): 'S',
  (DIT, DIT, DAH): 'U',
  (DIT, DAH, DIT): 'R',
  (DIT, DAH, DAH): 'W',
  (DAH, DIT, DIT): 'D',
  (DAH, DIT, DAH): 'K',
  (DAH, DAH, DIT): 'G',
  (DAH, DAH, DAH): 'O',
  (DIT, DIT, DIT, DIT): 'H',
  (DIT, DIT, DIT, DAH): 'V',
  (DIT, DIT, DAH, DIT): 'F',
  (DIT, DAH, DIT, DIT): 'L',
  (DIT, DAH, DAH, DIT): 'P',
  (DIT, DAH, DAH, DAH): 'J',
  (DAH, DIT, DIT, DIT): 'B',
  (DAH, DIT, DIT, DAH): 'X',
  (DAH, DIT, DAH, DIT): 'C',
  (DAH, DIT, DAH, DAH): 'Y',
  (DAH, DAH, DIT, DIT): 'Z',
  (DAH, DAH, DIT, DAH): 'Q',
  (DAH, DAH, DAH, DAH, DAH): '0',
  (DIT, DAH, DAH, DAH, DAH): '1',
  (DIT, DIT, DAH, DAH, DAH): '2',
  (DIT, DIT, DIT, DAH, DAH): '3',
  (DIT, DIT, DIT, DIT, DAH): '4',
  (DIT, DIT, DIT, DIT, DIT): '5',
  (DAH, DIT, DIT, DIT, DIT): '6',
  (DAH, DAH, DIT, DIT, DIT): '7',
  (DAH, DAH, DAH, DIT, DIT): '8',
  (DAH, DAH, DAH, DAH, DIT): '9',
  (DAH, DIT, DIT, DAH, DIT): '/',
  (DAH, DIT, DIT, DIT, DAH): '--',
  (DAH, DIT, DAH, DAH, DIT): '(',
  (DAH, DIT, DAH, DAH, DIT, DAH): ')',
  (DIT, DAH, DIT, DAH, DIT): '+',
  (DIT, DAH, DIT, DAH, DIT, DAH): '.',
  (DAH, DAH, DIT, DIT, DAH, DAH): ',',
  (DAH, DAH, DAH, DIT, DIT, DIT): ':',
  (DIT, DIT, DAH, DAH, DIT, DIT): '?',
  (DAH, DIT, DAH, DIT, DAH, DAH): '!',
  (DIT, DAH, DAH, DAH, DAH, DIT): "'",
  (DIT, DAH, DIT, DIT, DAH, DIT): '"',
  (DAH, DIT, DIT, DIT, DIT, DAH): '-',
  (DIT, DIT, DAH, DIT, DIT, DIT, DAH): '$',
}


class Morser:

  def __init__(
    self,
    dit=0.2,
    dah_multiple=2.5,
    intra_char=1.5,
    char_space=4.0,
    word_space=15.0,
    recent_buffer_size=8,
    dit_threshold=0.05,
    dah_threshold=0.1
    ):
    self.led = digitalio.DigitalInOut(board.GP25)
    self.led.direction = digitalio.Direction.OUTPUT
    self.dit = dit
    self.dah_multiple = dah_multiple
    self.dah = self.dit * self.dah_multiple
    self.intra_char = self.dit * intra_char
    self.char_space = self.dit * char_space
    self.word_space = self.dit * word_space
    self.recent_dits = []
    self.recent_dahs = []
    self.recent_buffer_size = recent_buffer_size
    self.char_buffer = []
    self.word_buffer = []
    self.dit_threshold = dit_threshold
    self.dah_threshold = dah_threshold

    print(f'Initial DIT: {self.dit:.2f}, DAH: {self.dah:.2f}')

    self.mark_start = None
    self.space_start = None
    self.was_mark = False
    self.in_mark = False

  def eval_mark(self, elapsed, mark_is_dit: bool):
    if mark_is_dit:
      mark = self.dit
      mark_word = DIT
      recent_marks = self.recent_dits
      threshold = self.dit_threshold
    else:
      mark = self.dah
      mark_word = DAH
      recent_marks = self.recent_dahs
      threshold = self.dah_threshold

    recent_marks.append(elapsed)

    if len(recent_marks) == 0:
      return mark

    if len(recent_marks) > self.recent_buffer_size:
      mean_mark = sum(recent_marks) / len(recent_marks)
      if mean_mark > 0 and abs(mean_mark - mark) > threshold:
        print(f'Adjusting {mark_word} from {mark:.2f} to {mean_mark:.2f}')
        mark = mean_mark

      mark_factor = len(recent_marks) // 2
      recent_marks = recent_marks[mark_factor:]

    if mark_is_dit:
      self.dit = mark
      self.recent_dits = recent_marks
    else:
      self.dah = mark
      self.recent_dahs = recent_marks
    return recent_marks

  def eval_dit(self, elapsed):
    self.char_buffer.append(DIT)
    self.eval_mark(elapsed, mark_is_dit=True)

  def eval_dah(self, elapsed):
    self.char_buffer.append(DAH)
    self.eval_mark(elapsed, mark_is_dit=False)

  def detect_cadence(self):
    if self.in_mark:
      self.led.value = True
      if not self.was_mark:
        # just entered a character
        self.mark_start = time.monotonic()
        if self.space_start:
          space_elapsed = time.monotonic() - self.space_start
          self.eval_space(space_elapsed)
      self.was_mark = True
    else:
      # dots in SPAAAAAAACE!!!
      self.led.value = False
      if self.was_mark:
        # just exited a character
        self.was_mark = False
        self.space_start = time.monotonic()
        if self.mark_start:
          mark_elapsed = time.monotonic() - self.mark_start
          if mark_elapsed >= self.dah * 0.7:
            self.eval_dah(mark_elapsed)
          elif mark_elapsed <= self.dit * 1.2:
            # was a dit
            self.eval_dit(mark_elapsed)
          else:
            print(f'NAH')
        self.was_mark = False
      else:
        # still in space
        # if timeout, evaluate space
        if self.space_start:
          space_elapsed = time.monotonic() - self.space_start
          if space_elapsed >= self.word_space * 2:
            self.eval_space(space_elapsed)
            self.space_start = None


  def eval_space(self, space_elapsed):
    if space_elapsed >= self.word_space * 0.7:
      self.eval_word()
    elif space_elapsed >= self.char_space * 0.7:
      self.eval_char()

  def eval_word(self):
    self.eval_char()
    print()
    self.word_buffer.clear()
    self.char_buffer.clear()

  def eval_char(self):
    char = MORSE[tuple(self.char_buffer)] if tuple(self.char_buffer) in MORSE else '?'
    print(char, end='')
    self.char_buffer.clear()
    self.word_buffer.append(char)

  def blink_and_beep(self):
    button = digitalio.DigitalInOut(board.GP15)
    button.switch_to_input(pull=digitalio.Pull.UP)

    buzzer = pwmio.PWMOut(board.GP11, duty_cycle=0, frequency=710)

    while True:
      self.loop(button, buzzer)

  def loop(self, button: DigitalInOut, buzzer: PWMOut):
    button_is_pulled_up = button.value
    self.in_mark = not button_is_pulled_up
    if not button_is_pulled_up:
      # buzzer.duty_cycle = 16384  # 25% duty cycle
      buzzer.duty_cycle = 32768  # 50% duty cycle
      # buzzer.duty_cycle = 49152  # 75% duty cycle
    else:
      buzzer.duty_cycle = 0
    self.detect_cadence()
    time.sleep(0.01)


if __name__ == '__main__':
  m = Morser(dit=0.1)
  m.blink_and_beep()
