import decimal
from datetime import timedelta

WEEK = timedelta(days=7)
DAY = timedelta(days=1)


class Allowance:
  def __init__(self, rate, period):
    self.rate = rate
    self.period = period

  def __str__(self):
    return f'${self.rate:,.2f} per {self.period}'


class Account:
  def __init__(self, holder, allowance):
    self.holder = holder
    self.allowance = allowance

  def __str__(self):
    return f'{self.holder}: {self.allowance}'


class Period:
  def __init__(self, account, start_date, duration):
    self.account = account
    self.start_date = start_date
    self.duration = duration

  @staticmethod
  def start_period(account, start_date, duration):
    return Period(account, start_date, duration=timedelta(days=7))


class Penalty:
  def __init__(self, price):
    self.amount = price


class Book:
  def __init__(self, accounts=None):
    self.accounts = accounts or {
      'Kid1': Account('Kid1', Allowance(12.00, WEEK)),
      'Kid2': Account('Kid2', Allowance(6.00, WEEK)),
    }

  def __str__(self):
    s = ''
    for account in self.accounts.values():
      s += f'{account}\n'
    return s


if __name__ == '__main__':
  book = Book()
  print(book)
