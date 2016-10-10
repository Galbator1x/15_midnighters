from datetime import datetime

from pytz import timezone
import requests


def load_attempts():
    url = 'https://devman.org/api/challenges/solution_attempts/'
    page, pages = 1, 1
    while page < pages + 1:
        payload = {'page': page}
        req = requests.get(url, params=payload).json()
        pages = req['number_of_pages']
        for record in req['records']:
            if record['timestamp'] is None:
                continue
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }
        page += 1


def get_midnighters():
    midnighters = set()
    for record in load_attempts():
        tz = timezone(record['timezone'])
        dt = tz.localize(datetime.utcfromtimestamp(record['timestamp']))
        dt_00 = tz.localize(datetime(dt.year, dt.month, dt.day, 0, 0, 0))
        dt_06 = tz.localize(datetime(dt.year, dt.month, dt.day, 6, 0, 0))
        if dt_00 < dt < dt_06:
            midnighters.add(record['username'])
    return midnighters


if __name__ == '__main__':
    print('Midnighters:')
    [print(name) for name in get_midnighters()]
