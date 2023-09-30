import requests

a_url = 'https://www.bellsystemmemorial.com/bell_logos.html'

response = requests.get(a_url)

page = response.text

all_number_signs = [page.find('#')]

print(page[all_number_signs[-1:]:all_number_signs[]

while '#' in page[all_number_signs[-1]:]:
  all_number_signs.append(page.find('#'))

for loc in all_number_signs:
  print(page[loc-20:loc+50])

