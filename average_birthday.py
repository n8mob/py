from datetime import datetime

day_of_year = datetime.now().timetuple().tm_yday
print(f'{day_of_year}')

birthdays = datetime.datetime('1976-12-26')
print(birthdays)
