import json
import random
import time
import requests
import pprint
from read_csv import read_csv

my_data = []


def get_TBL(res, art):
    for i in res.json()['data']['TBL']['FIRSTDATA']:
        for j in i['NAMES']:
            for u in j['PARAMS']:
                my_data.append({
                    'Артикль' : art,
                    'Name': u['NAME'],
                    'BRAND': u['BRAND'],
                    'QTY': u['RVALUE'],
                    'RSTP': u['RSTP'],
                    'ARTID': u['ARTID'],
                    'PARNR': u['PARNR'],
                    'PRICES1': u['PRICES1'],
                    'PRICEW1': u['PRICEW1'],
                    'Возврат товара': u['RETDAYS'],
                    'Склад': u['SNAME'],
                    'COMMENT': u['COMMENT'],
                    'WAERS': u['WAERS'],
                    'Поставка': u['SECURED_DAYS'],
                    'PIN': u['PIN'],
                    'BCODE': u['BCODE'],
                    'IMAGES_FULL': u['IMAGES_FULL']
                })


def get_SRCDATA(res, art):
    for i in res.json()['data']['TBL']['SRCDATA']:
        for j in i['NAMES']:
            for u in j['PARAMS']:
                my_data.append({
                    'Артикль': art,
                    'Name': u['NAME'],
                    'BRAND': u['BRAND'],
                    'QTY': u['RVALUE'],
                    'RSTP': u['RSTP'],
                    'Замена': f"{'Искомое' if u['RSTP'] == '0' else 'Замена для',article[0]}",
                    'ARTID': u['ARTID'],
                    'PARNR': u['PARNR'],
                    'PRICES1': u['PRICES1'],
                    'PRICEW1': u['PRICEW1'],
                    'Возврат товара': u['RETDAYS'],
                    'Склад': u['SNAME'],
                    'COMMENT': u['COMMENT'],
                    'WAERS': u['WAERS'],
                    'Поставка': u['SECURED_DAYS'],
                    'PIN': u['PIN'],
                    'BCODE': u['BCODE'],
                    'IMAGES_FULL': u['IMAGES_FULL']
                })


articles = read_csv('_SELECT_ps_part_number_pb_name_FROM_product_skus_ps_INNER_JOIN_p.csv')

cookies = {
    'ci_sessions': '8aicvqinu7uuf811eiuaetn3v2ldi9cb',
    'REMMEID': '54b7b766c36baea01824cd1f8ab7b12a',
    'VKORG': '8000',
    'rPrice': '0',
    '_ym_uid': '1724249685411255589',
    '_ym_d': '1724249685',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'ci_sessions=8aicvqinu7uuf811eiuaetn3v2ldi9cb; REMMEID=54b7b766c36baea01824cd1f8ab7b12a; VKORG=8000; rPrice=0; _ym_uid=1724249685411255589; _ym_d=1724249685; _ym_isad=1; _ym_visorc=w',
    'Origin': 'https://www.etp.armtek.kz',
    'Referer': 'https://www.etp.armtek.kz/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

for article in articles:
    time.sleep(random.randint(3, 7))

    print(article[0])
    try:
        data = {
            'QUERY': article[0],
            'QUERY_TYPE': '1',
            'QUERY_DATA': 'S1',
            'QUERY_HYSTORY': article[0],
            'OPTRS': 'true',
            'PKW': '',
            'LKW': '',
            'VIEW': 'short',
            'GROUP': '0',
            'ZZSING': 'S',
            'cashKey': '',
            'page': '1',
            'TTLLN': '152',
            'SRCNT': '44',
            'FORMAT': 'json',
            'LANG': 'ru',
        }

        response = requests.post(
            'https://www.etp.armtek.kz/search/getArticlesBySearch/?0.9636867307279298',
            cookies=cookies,
            headers=headers,
            data=data,
        )
        try:
            if response.json()['data']['TBL']['SRCDATA']:
                get_SRCDATA(response, article[0])
        except:
            print('TBL')
            get_TBL(response, article[0])

    except:
        print("Error")
        continue
with open('my_data.json', 'w') as f:
    json.dump(my_data, f, ensure_ascii=False, indent=4)
