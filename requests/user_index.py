import re
import json
from urllib.parse import quote

import requests

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}
session = requests.Session()



def get_token(screen_name):
    """
    获取游客token
    """
    url = f'https://twitter.com/{screen_name}'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',}
    response = session.get(url, headers=headers, proxies=proxies)
    token = re.findall(r'decodeURIComponent\("gt=(\d+);', response.text)
    print(token)
    return token[0]


screen_name = 'potus'
params = {
    'screen_name': screen_name,
    'withSafetyModeUserFields': False,
    'withSuperFollowsUserFields': False,
}
url = f'https://twitter.com/i/api/graphql/_Eo_tPE2WYM3C3gar4jwig/UserByScreenName?variables={quote(json.dumps(params, separators=(",", ":")))}'
print(url)
print('-' * 100)
headers = {
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'x-guest-token': '1424211390445752323',    
}

response = requests.get(url, headers=headers, proxies=proxies)
print(response.text)
print('-' * 100)
print(response.status_code)


# if __name__ == '__main__':
#     # token = get_token('potus')
