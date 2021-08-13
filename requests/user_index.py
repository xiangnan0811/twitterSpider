import os
import sys
import re
import json
from datetime import datetime
from urllib.parse import quote

import requests

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, BASE_DIR)

from db.concatSQL import get_insert_and_update_sql
from db.easyMySQL import EasyMySQL


def get_token(screen_name, session):
    """
    获取游客token
    """
    url = f'https://twitter.com/{screen_name}'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',}
    response = session.get(url, headers=headers, proxies=proxies)
    token = re.findall(r'decodeURIComponent\("gt=(\d+);', response.text)
    print(token)
    return token[0]


def get_user_info(screen_name, token, session):
    """
    获取用户基本信息
    """
    params = {
        'screen_name': screen_name,
        'withSafetyModeUserFields': False,
        'withSuperFollowsUserFields': False,
    }
    url = f'https://twitter.com/i/api/graphql/_Eo_tPE2WYM3C3gar4jwig/UserByScreenName?variables={quote(json.dumps(params, separators=(",", ":")))}'
    headers = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'x-guest-token': token,
    }
    response = session.get(url, headers=headers, proxies=proxies)
    return response


def get_resp_json(resp):
    """
    将response转换为json
    """
    try:
        return json.loads(resp.text)
    except json.decoder.JSONDecodeError:
        return None


def parse_user_response(data):
    """
    解析用户接口返回结果
    """
    user = data.get('data', {}).get('user', {}).get('result', {})
    # twitter 返回的 id 不是数字，猜测是用户唯一标识
    _id = user.get('id', '')
    if not _id:
        return {}
    # twitter 返回的用户ID，纯数字
    rest_id = user.get("rest_id", '')
    # 用户其余信息 legacy
    legacy = user.get("legacy", {})
    # 注册时间
    created_at = legacy.get("created_at", 0)
    if created_at:
        created_at = int(datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y").timestamp())
    # 简介
    description = legacy.get("description", '')
    # fast_followers_count
    fast_followers_count = legacy.get("fast_followers_count", 0)
    # 喜欢数
    favourites_count = legacy.get("favourites_count", 0)
    # 粉丝数
    followers_count = legacy.get("followers_count", 0)
    # 关注数
    friends_count = legacy.get("friends_count", 0)
    # 收听数
    listed_count = legacy.get("listed_count", 0)
    # 位置
    location = legacy.get("location", '')
    # 图片视频数
    media_count = legacy.get("media_count", 0)
    # 昵称
    name = legacy.get("name", '')
    # 正常粉丝数
    normal_followers_count = legacy.get("normal_followers_count", 0)
    # 主页横幅图
    profile_banner_url = legacy.get("profile_banner_url", '')
    # 头像
    profile_image_url = legacy.get("profile_image_url_https", '')
    # screen_name
    screen_name = legacy.get("screen_name", '')
    # statuses_count
    statuses_count = legacy.get("statuses_count", 0)

    return {
        'id': _id,
        'rest_id': rest_id,
        'created_at': created_at,
        'description': description,
        'fast_followers_count': fast_followers_count,
        'favourites_count': favourites_count,
        'followers_count': followers_count,
        'friends_count': friends_count,
        'listed_count': listed_count,
        'location': location,
        'media_count': media_count,
        'name': name,
        'normal_followers_count': normal_followers_count,
        'profile_banner_url': profile_banner_url,
        'profile_image_url': profile_image_url,
        'screen_name': screen_name,
        'statuses_count': statuses_count,
    }


if __name__ == '__main__':
    screen_name = 'potus'
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }
    session = requests.Session()
    token = get_token(screen_name, session)
    resp = get_user_info(screen_name, token, session)
    data = get_resp_json(resp)
    user = parse_user_response(data)
    print(user)
    print("-" * 100)
    insert_sql = f'''INSERT INTO user({', '.join(user.keys())}) VALUES({', '.join(list(map(lambda x: f'"{x}"', user.values())))})'''
    print(insert_sql)
    easy_mysql = EasyMySQL('47.108.151.116', 19412, 'root', '13720929258Ber*', 'twitter')
    # easy_mysql.connect()
    insert_result = easy_mysql.insert(insert_sql)
    print('-' * 100)
    print(insert_result)
    # res = easy_mysql.get_all('select * from twitter.user')
    # print(res)

