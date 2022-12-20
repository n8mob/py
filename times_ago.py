import argparse
from datetime import datetime, timezone, timedelta
from dateutil.parser import parse

import dateutil

if __name__ == '__main__':
    options = argparse.ArgumentParser()
    options.add_argument('then', type=parse)
    options.parse_args()
    args = options.parse_args()

    mst = timezone(timedelta(hours=-7))

    that_was_then: datetime = args.then
    this_is_now: datetime = datetime.now(mst)

    total_seconds = (this_is_now - that_was_then).total_seconds()
    minutes_ago, seconds_ago = divmod(total_seconds, 60)

    print(f'{that_was_then} was {minutes_ago:.0f}m {seconds_ago:.0f}s ago')
