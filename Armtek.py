import csv
import json
import random
import time
import requests


class Armtek:
    MY_DATA = []
    HEADERS = {
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

    def __init__(self, articles, cookies):
        self.articles = articles
        self.cookies = cookies

    def _write_content(self):
        with open('my_data.json', 'w') as f:
            json.dump(self.MY_DATA, f)

    def _read_articles(self, path):
        articles = []
        with open(path, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row:
                    articles.append(row[0])
        return articles

    def _read_brand(self, path):
        articles = []
        with open(path, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row:
                    articles.append(row[1])
        return articles


    def __get_TBL(self, req, article):
        for i in req.json()['data']['TBL']['FIRSTDATA']:
            for j in i['NAMES']:
                for u in j['PARAMS']:
                    self.MY_DATA.append({
                        'Артикль': article,
                        'Name': u['NAME'],
                        'BRAND': u['BRAND'],
                        'QTY': u['RVALUE'],
                        'RSTP': u['RSTP'],
                        'Замена': f"{'Искомое' if u['RSTP'] == '0' else 'Замена для', article}",
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

    def __get_SRCDATA(self, req, article):
        for i in req.json()['data']['TBL']['SRCDATA']:
            for j in i['NAMES']:
                for u in j['PARAMS']:
                    self.MY_DATA.append({
                        'Артикль': article,
                        'Name': u['NAME'],
                        'BRAND': u['BRAND'],
                        'QTY': u['RVALUE'],
                        'RSTP': u['RSTP'],
                        'Замена': f"{'Искомое' if u['RSTP'] == '0' else 'Замена для', article}",
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

    def run(self, articles=None, write='OFF',
            QUERY_TYPE = "1",
            QUERY_DATA='S1',
            TTLLN="152",
            SRCNT='44'
            ):
        if articles is None:
            articles = self._read_articles(self.articles)
        print(len(articles))
        for article in articles:
            time.sleep(random.randint(2, 4))
            print(f'Ищу арт.{article}')
            try:
                data = {
                    'QUERY': article,
                    'QUERY_TYPE': QUERY_TYPE,
                    'QUERY_DATA': QUERY_DATA,
                    'QUERY_HYSTORY': article,
                    'OPTRS': 'true',
                    'PKW': '',
                    'LKW': '',
                    'VIEW': 'short',
                    'GROUP': '0',
                    'ZZSING': 'S',
                    'cashKey': '',
                    'page': '1',
                    'TTLLN': TTLLN,
                    'SRCNT': SRCNT,
                    'FORMAT': 'json',
                    'LANG': 'ru',
                }

                response = requests.post(
                    'https://www.etp.armtek.kz/search/getArticlesBySearch/?0.9636867307279298',
                    cookies=self.cookies,
                    headers=self.HEADERS,
                    data=data,
                )
                try:
                    if response.json()['data']['TBL']['SRCDATA']:
                        self.__get_SRCDATA(response, article)
                except:
                    self.__get_TBL(response, article)

            except Exception as Ex:
                if Ex.__str__().strip() == 'list indices must be integers or slices, not str':
                    print(f'Art not found! {article} \n {Ex}')
                else:
                    print(f'Неизвесная ошибка \n {Ex}')
                continue
        if write == 'ON':
            self._write_content()

    def run_2(self):
        brands = self._read_brand(self.articles)
        new_articles = []
        self.run()
        for brand in brands:
            for i in self.MY_DATA:
                if i.get('BRAND') == brand:
                    new_articles.append(i.get('ARTID'))
        self.MY_DATA.clear()
        self.run(articles=new_articles, write='ON', QUERY_TYPE="5", QUERY_DATA='S2', TTLLN='35', SRCNT='19')



