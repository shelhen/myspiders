import requests
import json
import random
import time


class XueSpider(object):
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            "Accept":"application/json, text/plain, */*",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        self.base_url ="https://xueqiu.com/statuses/hot/listV2.json"

    def get_xhr(self, max_id):
        params={ "since_id": "-1", "max_id": max_id, "size":"15"}
        response = self.session.get(url=self.base_url, params=params, timeout=10, headers=self.headers)
        return response.json()

    def parse(self, datas):
        return [{
            'id':item['id'],
            'description':item['original_status']['description'],
            'title':item['original_status']['title']
        } for item in datas['items']]

    def main(self):
        path = r"./datas/雪球资讯.json"
        max_id = 517045
        results = []
        self.session.get('https://xueqiu.com/', headers=self.headers, timeout=10)
        for i in range(20):
            time.sleep(3 + 5*random.random())
            max_id = max_id-15
            datas = self.get_xhr(max_id)
            result = self.parse(datas)
            for r in result:
                print(r)
            results.extend(result)
        json.dump(results, open(path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)


if __name__ == '__main__':
    xs = XueSpider()
    xs.main()
