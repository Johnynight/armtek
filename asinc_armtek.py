import csv
import json
import random
import asyncio
import aiohttp
import ssl
import certifi

sslcontext = ssl.create_default_context(cafile=certifi.where())


class Armtek:
    MY_DATA = []
    HEADERS = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
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

    async def _write_content(self):
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

    def __get_TBL(self, data, article):
        for i in data['data']['TBL']['FIRSTDATA']:
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

    def __get_SRCDATA(self, data, article):
        for i in data['data']['TBL']['SRCDATA']:
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

    async def _fetch_article(self, session, article, QUERY_TYPE, QUERY_DATA, TTLLN, SRCNT):
        await asyncio.sleep(random.randint(2, 4))
        print(f'Ищу арт.{article}')
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

        try:
            async with session.post(
                    'https://www.etp.armtek.kz/search/getArticlesBySearch/?0.9636867307279298',
                    cookies=self.cookies,
                    headers=self.HEADERS,
                    data=data,
                    ssl=sslcontext
            ) as response:
                result = await response.json()
                try:
                    if result['data']['TBL']['SRCDATA']:
                        self.__get_SRCDATA(result, article)
                except:
                    self.__get_TBL(result, article)

        except Exception as Ex:
            if str(Ex).strip() == 'list indices must be integers or slices, not str':
                print(f'Art not found! {article} \n')
            else:
                print(f'Неизвесная ошибка \n {Ex}')

    async def run(self, articles=None, write='OFF',
                  QUERY_TYPE="1", QUERY_DATA='S1',
                  TTLLN="152", SRCNT='44'):
        if articles is None:
            articles = self._read_articles(self.articles)
        print(len(articles))

        async with aiohttp.ClientSession() as session:
            tasks = [
                self._fetch_article(session, article, QUERY_TYPE, QUERY_DATA, TTLLN, SRCNT)
                for article in articles
            ]
            await asyncio.gather(*tasks)

        if write == 'ON':
            await self._write_content()

    async def run_2(self):
        brands = self._read_brand(self.articles)
        new_articles = []
        await self.run()
        for brand in brands:
            # await asyncio.sleep(2)
            for i in self.MY_DATA:
                if i.get('BRAND') == brand:
                    new_articles.append(i.get('ARTID'))
        self.MY_DATA.clear()
        await self.run(articles=new_articles, write='ON', QUERY_TYPE="5", QUERY_DATA='S2', TTLLN='35', SRCNT='19')

