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
from parser.parser import get_user_item


def get_token(screen_name, session, proxies):
    """
    获取游客token
    """
    url = f'https://twitter.com/{screen_name}'
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',}
    response = session.get(url, headers=headers, proxies=proxies)
    token = re.findall(r'decodeURIComponent\("gt=(\d+);', response.text)
    return token[0]


def get_user_info(screen_name, token, session, proxies):
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


def main(screen_name, mysql_connection, proxies):
    """
    主函数
    """
    session = requests.Session()
    token = get_token(screen_name, session, proxies)
    user_resp = get_user_info(screen_name, token, session, proxies)
    user_data = get_resp_json(user_resp)
    user, user_id = get_user_item(user_data)
    print(user_id)
    if user:
        user_sql = get_insert_and_update_sql(user, 'twitter', 'user')
        user_result = mysql_connection.insert(user_sql)
        print(user_result)
        print('*' * 100)


if __name__ == '__main__':
    users = ['realdonaldtrump', 'potus', 'BarackObama', 'mike_pence', 'vp', 'JoeBiden', 'esperdod', 'stevenmnuchin1', 'SecretaryCarson', 'SecPompeo', 'dhs_wolf', 'SpeakerPelosi', 'agwilliambarr', 'secbernhardt', 'MickMulvaneyOMB', 'sentoddyoung', 'toddyoungin', 'SenatorRisch', 'marcorubio', 'senhawleypress', 'hawleymo', 'chuckschumer', 'senatordurbin', 'markwarner', 'senjeffmerkley', 'senatorleahy', 'senatemajldr', 'senjohnthune', 'ewarren', 'berniesanders', 'johnboozman', 'sentomcotton', 'senfeinstein', 'kamalaharris', 'sencorygardner', 'chrismurphyct', 'chriscoons', 'marcorubio', 'senrickscott', 'sendavidperdue', 'brianschatz', 'chuckgrassley', 'senangusking', 'senatorcardin', 'chrisvanhollen', 'senmarkey', 'senatorwicker', 'senatortester', 'stevedaines', 'senatorfischer', 'sensasse', 'senatorshaheen', 'senatormenendez', 'corybooker', 'senjohnhoeven', 'sensherrodbrown', 'jiminhofe', 'senatorlankford', 'ronwyden', 'sentoomey', 'senjackreed', 'lindseygrahamsc', 'johncornyn', 'SenTedCruz', 'senatorromney', 'edanoyukio0531', 'shiikazuo', 
'sugawitter', 'moteging', 'nodayoshi55', 'saitou_ken', 'heikomaas', 'mvenkaiahnaidu', 'vpsecretariat', 'jeremy_hunt', 'dominicraab', 'steinmeier_f_w', 'frankwalterste3', 'chefsteinmeier', 'angelamerkeicdu', 'queen_europe', 'mattarella1', 'sergiomattarel4', 'giorgionapolit4', 'napolitano_bis', 'giorgionapolit5', 'g_napolitanobis', 'giuseppeconteit', 'paologentiloni', 'emmanuelmacron', 'fhollande', 'ephilippepm', 'bcazeneuve', 'borisjohnson', 'ramnathkovindfc', 'rashtrapatibhvn', 'pmoindia', 'narendramodi', 'abeshinzo', 'aso_tarou', 'tadamori_oshima', 'moonriver365', 'moonjaein_news', 'thebluehouseeng', 'moonhstw', 'gh_park', 'swedishpm', 'fredrikreinfelt', 'plaid_reinfeldt', 'freinfeldt', 'margotwallstrom', 'repmcgovern', 'skinnock', 'tomtugendhat', 'henrysmithuk', 'miriammlex', 'marisepayne', 'repmccaul', 'fp_champagne', 'senatorwong', 'winstonpeters', 'uffeelbaek', 'mariearenaps', 'repfrenchhill', 'marshablackburn', 'ianbremmer', 'lpnorthover', 'pennymordaunt', 'catherinewest1', 'natalieben', 'jkenney', 'erinotoolemp', 'kimbakit', 'guyverhofstadt', 'mpwangtingyu', 'maxferrari', 'cvoule', 'neildotobrien', 'bueti', 'jtrittin', 'grimoldipaolo', 'adomenas', 'cafreeland', 'gydej', 'alfonslopeztena', 'sarahchampionmp', 'amcarmichaelmp', 'pmcroninhudson', 'dooley_dooley', 'brendancarrfcc', 'senatorhousakos', 'jackposobiec', 'repjimbanks', 'repdlamborn', 'replahood', 'vibattueuspox', 'bradsherman', 'repmarkgreen', 'replamalfa', 'greschenthaler', 'garnettgenuis', 'repscottperry', 'reptedyoho', 'gopleader', 'reptomsuozzi', 'repmichaelwaltz', 'desjarlaistn04', 'stewartmcdonald', 'satomasahisa', 'repgallagher', 'rep_stevewomack', 'replowenthal', 'senatormunson', 'engineroglu_fw', 'goeringeckardt', 'margaretebause', 'simonclarkemp', 'leaderhoyer', 'repstevechabot', 'drl_as', 'pauljsweeney', 'repriggleman', 'repharley', 'usambun', 'repjohncurtis', 'michaelcburgess', 'dkshrewsbury', 'robert_aderholt', 'jvanovertveldt', 'replipinski', 'andrew_adonis', 'barrysheerman', 'tobias_ellwood', 'mpritcharduk', 'mpiainds', 'lisanandy', 'gwynnemp', 'senpaterson', 'navpmishra', 'davidsweetmp', 'senmcsallyaz', 'iowbobseely', 'AlynSmith', 'lancegooden', 'mikebarretton', 'senatorbennet', 'imranahmadkhan', 'moritzkoerner', 'robertcobrien', 'andrewbowie_mp', 'AndriusKubilius', 'yamazogaikuzo', 'theliberalfrank', 'sven_giegold', 'shioriyamao', 'DjirSarai', 'gary_srp', 'patkelly_mp', 'rjukneviciene', 'egebhardtmdep', 'jamie4north', 'adambandt', 'carolinelucas', 'hjaruissen', 'nagashima21', 'replloyddoggett', 'ruthdavidsonmsp', 'andrewscheer', 'nikkihaley', 'senjohnkennedy', 'tomkmiec', 'charlesmichel', 'laylamoran', 'matsubarajin731', 'otokita', 'kellyblockmp', 'sarahinthesen8', 'dereksloancpc', 'terryreintke', 'alexbazzaro']
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }
    easy_mysql = EasyMySQL('host', 0, 'user', 'password', 'db')
    print(len(users))
    for user in users:
        main(user, mysql_connection=easy_mysql, proxies=proxies)


