import time
import board
import digitalio
import pwmio
from digitalio import DigitalInOut, DriveMode
from pwmio import PWMOut


class Morser:
  def __init__(
    self,
    dit=0.1,
    dah_multiple=2.5,
    intra_char=1.5,
    char_space=3.0,
    word_space=6.5,
    recent_buffer_size=5,
    dit_threshold=0.05,
    dah_threshold=0.1
    ):
    self.dit = dit
    self.dah_multiple = dah_multiple
    self.dah = self.dit * self.dah_multiple
    self.intra_char = intra_char
    self.char_space = char_space
    self.word_space = word_space
    self.recent_dits = []
    self.recent_dahs = []
    self.recent_buffer_size = recent_buffer_size
    self.dit_threshold = dit_threshold
    self.dah_threshold = dah_threshold

    self.mark_start = None
    #self.space_start = None
    self.was_char = False
    self.in_char = False

  def eval_mark(self, elapsed, mark_is_dit: bool):
    if mark_is_dit:
      mark = self.dit
      recent_marks = self.recent_dits
      threshold = self.dit_threshold
    else:
      mark = self.dah
      recent_marks = self.recent_dahs
      threshold = self.dah_threshold

    if len(recent_marks) == 0:
      return mark

    recent_marks.append(elapsed)
    if len(recent_marks) > self.recent_buffer_size:
      recent_marks.pop(0)
    mean_mark = sum(recent_marks) / len(recent_marks)
    if mean_mark > 0 and mean_mark - mark > threshold:
      mark = mean_mark

    if mark_is_dit:
      self.dit = mark
    else:
      self.dah = mark
    return mark

  def eval_dit(self, elapsed):
    print(f'DIT: {elapsed:.2f}')
    return self.eval_mark(elapsed, mark_is_dit=True)

  def eval_dah(self, elapsed):
    print(f'DAH: {elapsed:.2f}')
    return self.eval_mark(elapsed, mark_is_dit=False)

  def detect_cadence(self):
    if self.in_char:
      if not self.was_char:
        # just entered a character
        self.mark_start = time.monotonic()
        self.was_char = True
    else:
      if self.was_char:
        # just exited a character
        self.in_char = False
        elapsed = time.monotonic() - self.mark_start
        if elapsed < (self.dit + self.dit * self.intra_char) / 2:
          self.eval_dit(elapsed)
        else:
          self.eval_dah(elapsed)
        self.was_char = False
    pass


  def blink_and_beep(self):
    led = digitalio.DigitalInOut(board.GP25)
    led.direction = digitalio.Direction.OUTPUT

    button = digitalio.DigitalInOut(board.GP15)
    button.switch_to_input(pull=digitalio.Pull.UP)

    buzzer = pwmio.PWMOut(board.GP11, duty_cycle=0, frequency=710)

    while True:
      self.loop(button, buzzer, led)

  def loop(self, button: DigitalInOut, buzzer: PWMOut, led: DigitalInOut):
    button_is_pulled_up = button.value
    self.in_char = not button_is_pulled_up
    if not button_is_pulled_up:
      # buzzer.duty_cycle = 16384  # 25% duty cycle
      # buzzer.duty_cycle = 32768  # 50% duty cycle
      buzzer.duty_cycle = 49152  # 75% duty cycle
      led.value = True
    else:
      buzzer.duty_cycle = 0
      led.value = False
    self.detect_cadence()
    time.sleep(0.01)


if __name__ == '__main__':
  m = Morser()
  m.blink_and_beep()
