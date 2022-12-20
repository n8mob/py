#!/usr/bin/env python3

import argparse
import calendar
import datetime
import sys
from datetime import datetime as dt
import shutil

ALWAYS_PRINT_MONTH = "* %a, %b %-d"
DAY_OF_WEEK_HEADER = "* %A %-d"
ORG_FILE_NAME_FORMAT = '%m_%d.org'

c = calendar.Calendar(firstweekday=calendar.SUNDAY)


def weeks_and_files_for_month(year, month):
    weeks = [week for week in c.monthdatescalendar(year, month) if week[0].month == month]

    return [(week, dt.strftime(week[0], ORG_FILE_NAME_FORMAT)) for week in weeks]


def headers_for_days_of_week(week, always_print_month=False):
    for day in week:
        yield dt.strftime(day, ALWAYS_PRINT_MONTH if always_print_month else DAY_OF_WEEK_HEADER)


def prepare_month(year: int, month: int):
    for week in c.monthdatescalendar(year, month):
        week_is_from_last_month = week[0].month != month

        if not week_is_from_last_month:
            week_filename = dt.strftime(week[0], ORG_FILE_NAME_FORMAT)
            print(f'{week_filename} includes {", ".join(headers_for_days_of_week(week, always_print_month=True))}')


if __name__ == '__main__':
    today = dt.now().date()
    options = argparse.ArgumentParser()
    options.add_argument('-y', '--year', type=int, default=today.year)
    options.add_argument('-m', '--month', type=int, default=today.month)
    options.add_argument("--next-week", action='store_true')
    options.add_argument("--always-print-month", action='store_true')
    args = options.parse_args()

    main_year = args.year or today.year
    main_month = args.month or today.month

    if args.next_week:
        month_for_next_week = (today + datetime.timedelta(days=7)).month
        next_weeks_month = c.monthdatescalendar(today.year, today.month)
        next_week = None

        for main_week in next_weeks_month:
            if main_week[0] > today:
                next_week = main_week
                break

        if not next_week:
            print('there was a problem figuring out when next week starts')
            exit(1)

        for header in headers_for_days_of_week(next_week):
            print(header)

    else:
        weeks_for_month = weeks_and_files_for_month(main_year, main_month)
        for main_week, week_file_name in weeks_for_month:
            with open(week_file_name, 'w') as week_file:
                print(f'opened {week_file_name} in {week_file}')
                for header in headers_for_days_of_week(main_week):
                    week_file.write(header + '\n\n')
