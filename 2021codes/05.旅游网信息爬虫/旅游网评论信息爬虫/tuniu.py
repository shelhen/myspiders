import re,time
import requests
import random
from util import remark_save


class TuniuSpider(object):
    def __init__(self):
        self.headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }
        self.session = requests.session()
        self.p = re.compile(r'[^\w，。！？,.、:；℃]')
        self.ploids = [
            '1742595',  # 汉文化景区
            '3241',  # 龟山汉墓
            '3244'  # 云龙湖
        ]

    def get_commets(self,id,page):
        url = "https://m.tuniu.com/mapi/tour/getMenpiaoComment"
        ts = str(int(time.time()*1e6))+str(random.random())[2:]
        params={
            "specId": id,
            "currentPage": page,
            '_': ts
        }
        res = self.session.get(url, params=params, headers=self.headers, timeout=10)
        return res.json()['data']

    def parse(self, datas):
        remarks = [{
            "publishTime": time.mktime(time.strptime(data['remarkTime'], "%Y-%m-%d %H:%M:%S")),
            "score": int(round(int(data['compGrade'])*1.66, 0)),
            "content": self.p.sub("", data['content'].lower()),
            "Locate": '',
            "usefulCount": 0
        } for data in datas]
        return remarks

    def main(self):
        for id in self.ploids:
            # 获取总页数
            tatolNum = int(self.get_commets(id,1)['pageNums'])
            # commentCount = int(self.get_commets(id, 1)['total'])
            # tatolNum = commentCount // 10 if commentCount % 10 == 0 else (commentCount // 10) + 1
            for i in range(tatolNum):
                datas = self.get_commets(id, i+1)['remarkList']
                remarks = self.parse(datas)
                for remark in remarks:
                    print(remark)
                remark_save('tuniu',remarks)
            print(f'已完成id为{id}地区的评论爬取')


if __name__ == '__main__':
    tuniu=TuniuSpider()
    tuniu.main()