import base64
import re
from re import Match
"""
I typed in "I got a captcha..." and Copilot suggested the following summary:

> I got a captcha on Google and I'm trying to figure out what the hell is going on.
> I'm trying to decode the base64 strings in the URL, but I'm getting an error.
> Can you help me out?

So, Copilot suggested that I ask "Can you help me out?" X-D
"""


def decode_base64(data):
  # Add padding if necessary
  ld = len(data)
  missing_padding = ld % 4
  padded = data + ('=' * (4 - missing_padding))
  lp = len(padded)
  print(f'len(data)={ld}, len(padded)={lp}')
  if len(padded) % 4 != 0:
    raise ValueError('Invalid base64 string')

  return base64.b64decode(padded, validate=True)


weird_request = {
  "scheme": "https",
  "host": "www.google.com",
  "filename": "/search",
  "query": {
    "q": "sbarro",
    "sca_esv": "2c50b593bf3afd6b",
    "sca_upv": "1",
    "source": "hp",
    "ei": "5XLSZo2oJ_KekPIP-7emkQ4",
    "iflsig": "AL9hbdgAAAAAZtKA9XfyuX1KPIMrN9VnkDmopIAbH4aE",
    "ved": "0ahUKEwjNrsKNi56IAxVyD0QIHfubKeIQ4dUDCBA",
    "uact": "5",
    "oq": "sbarro",
    "gs_lp": "Egdnd3Mtd2l6IgZzYmFycm8yFhAuGIAEGLEDGNEDGEMYgwEYxwEYigUyCBAAGIAEGLEDMggQABiABBixAzILEC4YgAQYxwEYrwEyBRAAGIAEMgsQLhiABBjHARivATIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIu-kDUJ8FWIKlA3AFeACQAQCYAXSgAfAFqgEDMC43uAEDyAEA-AEBmAIMoALHBqgCCsICEBAAGIAEGEMYtAIYigUY6gLCAhYQLhiABBjRAxhDGLQCGMcBGIoFGOoCwgIWEC4YgAQYQxi0AhjHARiKBRjqAhivAcICEBAuGIAEGNEDGEMYxwEYigXCAgoQABiABBhDGIoFwgIQEC4YgAQYQxjHARiKBRivAcICChAuGIAEGEMYigXCAhEQLhiABBixAxjRAxiDARjHAcICCxAuGIAEGNEDGMcBwgINEAAYgAQYsQMYQxiKBcICCxAAGIAEGLEDGIMBwgIIEC4YgAQYsQOYAw6SBwM1LjegB7lO",
    "sclient": "gws-wiz"
  },
  "remote": {
    "Address": "[2607:f8b0:4005:810::2004]:443"
  }
}


def check_base64_re(data):
  base64_re = re.compile(r'^[A-Za-z0-9+/]*={0,2}$')
  return base64_re.match(data)



if __name__ == '__main__':
  for s in weird_request['query']['gs_lp'].split('-'):
    match = check_base64_re(s)
    if match:
      print(f'{s[:20]} match: {match.group()}')
    else:
      print(f'{s[:20]} no match')

