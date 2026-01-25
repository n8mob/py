import time
import board
import digitalio
import pwmio
from digitalio import DigitalInOut, DriveMode
from pwmio import PWMOut


class Morser:
  def __init__(
    self,
    dit=0.2,
    dah_multiple=2.5,
    intra_char=1.5,
    char_space=3.0,
    word_space=6.5,
    recent_buffer_size=8,
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

    print(f'Initial DIT: {self.dit:.2f}, DAH: {self.dah:.2f}')

    self.mark_start = None
    #self.space_start = None
    self.was_char = False
    self.in_char = False

  def eval_mark(self, elapsed, mark_is_dit: bool):
    if mark_is_dit:
      mark = self.dit
      mark_word = 'DIT'
      recent_marks = self.recent_dits
      threshold = self.dit_threshold
    else:
      mark = self.dah
      mark_word = 'DAH'
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
      print(f'Trimming {mark_factor} from recent {mark_word}s: {recent_marks}')

    if mark_is_dit:
      self.dit = mark
      self.recent_dits = recent_marks
    else:
      self.dah = mark
      self.recent_dahs = recent_marks
    return recent_marks

  def eval_dit(self, elapsed):
    print(f'DIT')
    return self.eval_mark(elapsed, mark_is_dit=True)

  def eval_dah(self, elapsed):
    print(f'DAH')
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
        print(f'{elapsed:.2f}', end=' ')
        if elapsed >= self.dah * 0.7:
          self.eval_dah(elapsed)
        elif elapsed <= self.dit * 1.2:
          # was a dit
          self.eval_dit(elapsed)
        else:
          print(f'NAH')
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
  m = Morser(dit=0.1)
  m.blink_and_beep()
