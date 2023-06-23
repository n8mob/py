from decimal import Decimal
from datetime import datetime

one = Decimal(1)
four = Decimal(4)


def attempt1():
    n = 1
    n = input('n? ')
    while str.isnumeric(n):
        n = int(n)
        pi = Decimal(3.0)

        is_neg = False

        for i in range(2, n, 2):
            id = Decimal(i)
            denom = id * id + 1 * id + 2
            term = four / denom
            if is_neg:
                pi -= term
            else:
                pi += term

            is_neg = not is_neg

        print(f'π = {pi}')
        n = input('n? ')


class Attempt2:
    def __init__(self, correct="3.141592653"):
        self.correct = correct
        self.current = ""
        self.current_pi_fourths = one
        self.i = 1
        self.do_subtract = True

    def increment(self):
        next_odd = Decimal(self.i * 2 + 1)
        term = one / next_odd

        if self.do_subtract:
            self.current_pi_fourths -= term
        else:
            self.current_pi_fourths += term
        self.do_subtract = not self.do_subtract
        self.i += 1

        self.current = str(self.current_pi_fourths * 4)

    def print_state(self):
        correct = self.current_correct()
        fourths = self.current_pi_fourths

        print(f'correct so far: {correct} current 𝜋/4: {fourths} iterations: {self.i:,}')

    @staticmethod
    def match_len(a, b):
        if len(a) < len(b):
            shorter = a
        else:
            shorter = b

        index = 0

        for index in range(len(shorter)):
            if a[index] != b[index]:
                return index
        return 0

    def max_matching(self, a, b):
        if len(a) < len(b):
            shorter = a
        else:
            shorter = b

        return shorter[:self.match_len(a, b)]

    def print_match(self):
        print(self.current_correct())

    def current_correct(self):
        return self.max_matching(self.correct, self.current)


if __name__ == '__main__':
    a2 = Attempt2(correct='3.141592653589793238462643383')

    start_time = datetime.now()
    elapsed_seconds = 0

    while len(a2.current_correct()) < 8:
        previous_match = len(a2.current_correct())
        increments_before_report = 200
        while len(a2.current_correct()) <= previous_match:
            for i in range(increments_before_report):
                a2.increment()

            elapsed_seconds = (datetime.now() - start_time).total_seconds()

            print(f'\r{a2.i:<8,} iterations to {a2.current_correct()} ({elapsed_seconds} seconds)', end='', flush=True)

        print(f'\r', end='')
        print(f'{a2.i:<8,} iterations to {a2.current_correct()} ({elapsed_seconds} seconds)', flush=True)
        increments_before_report *= 100
