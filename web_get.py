import requests

response = requests.get(
  'https://computer.rip/2023-02-07-secret-government-telephone-numbers.html',
  headers={'Accepts': 'text/plain'})

print(response.text.split('\n')[78:83])

