#!/usr/bin/env python3

import argparse
import calendar
import datetime
import sys
from datetime import datetime as dt
import shutil

ORG_DAY_HEADER_FORMAT = "* %a, %b %-d"
ORG_FILE_NAME_FORMAT = '%m_%d.org'

c = calendar.Calendar(firstweekday=calendar.SUNDAY)


def weeks_and_files_for_month(year, month):
    weeks = [week for week in c.monthdatescalendar(year, month) if week[0].month == month]

    return [(week, dt.strftime(week[0], ORG_FILE_NAME_FORMAT)) for week in weeks]


def headers_for_days_of_week(week):
    for day in week:
        yield dt.strftime(day, ORG_DAY_HEADER_FORMAT)


def prepare_month(year: int, month: int):
    for week in c.monthdatescalendar(year, month):
        week_is_from_last_month = week[0].month != month

        if not week_is_from_last_month:
            week_filename = dt.strftime(week[0], ORG_FILE_NAME_FORMAT)
            print(f'{week_filename} includes {", ".join(headers_for_days_of_week(week))}')


if __name__ == '__main__':
    options = argparse.ArgumentParser()
    options.parse_args()

    if sys.argv and len(sys.argv) > 1:
        main_year = int(sys.argv[1])
    else:
        main_year = datetime.date.today().year

    main_month = 11

    month_name = calendar.month_name[main_month]
    print(f'Preparing files for the weeks in {month_name} {main_year}')

    weeks_for_month = weeks_and_files_for_month(main_year, main_month)
    for main_week, week_file_name in weeks_for_month:
        with open(week_file_name, 'w') as week_file:
            print(f'opened {week_file_name} in {week_file}')
            for header in headers_for_days_of_week(main_week):
                week_file.write(header + '\n\n')
