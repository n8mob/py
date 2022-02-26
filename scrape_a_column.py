from os.path import exists

import requests
from bs4 import BeautifulSoup

vhf_society_repeater_list_url = 'http://www.utahvhfs.org/rptr.html'
soup = {}
cached_request_path = 'page.cache.html'

if __name__ == '__main__':
    if not soup:
        print('no cached object')
        if exists(cached_request_path):
            print(f'reading file: {cached_request_path}')
            soup = BeautifulSoup(open(cached_request_path, 'r'), features='html.parser')
        else:
            print(f'no file, requesting from {vhf_society_repeater_list_url}')
            response = requests.get(vhf_society_repeater_list_url)
            print(f'response has encoding: {response.encoding}')
            f = open(cached_request_path, 'w')
            f.write(response.text)
            soup = BeautifulSoup(response.text, features='html.parser')

    print(f'Loaded HTML document: {soup.title.text}')

    two_meter_rows = soup.findAll('table')[3].findAllNext('tr')

    header_row = two_meter_rows[0]
    two_meter_rows = two_meter_rows[1:]

    table_headers = [th.text.replace('\xa0', ' ') for th in two_meter_rows[0].findAllNext('th')]

    ctcss_column_index = table_headers.index('CTCSS')

    a_row = two_meter_rows[10]
    print(f'{a_row.text=}')

    data_from_first_row = [td.text.replace('\xa0', ' ') for td in a_row.find_all('td')]

    print(f'{data_from_first_row=}')

    all_data = []

    for row in two_meter_rows:
        all_data.append([td.text.replace('\xa0', ' ') for td in row.find_all('td')])

    print(f'{len(all_data)=}')

    unique_ctcss_tones = {td[ctcss_column_index] for td in all_data if len(td) > ctcss_column_index}
    pl_tones = []
    for tone in unique_ctcss_tones:
        try:
            pl_tones.append(float(tone))
        except ValueError:
            ...

    pl_tones = sorted(pl_tones)

    print(f'{pl_tones=}')
