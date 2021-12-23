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
            f = open(cached_request_path, 'w')
            f.write(response.text)
            soup = BeautifulSoup(response.text, features='html.parser')

    print(soup.title)
