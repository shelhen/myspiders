import time, re
from util import remark_save
import requests


class QiongSpider(object):
    def __init__(self):
        self.headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }
        self.session = requests.session()
        self.p = re.compile(r'[^\w，。！？,.、:；℃]')
        self.ploids = [
            '1485376',  # 汉文化景区
            '1469634',  # 徐州博物馆
            '1485359',  # 龟山汉墓
            '1469637',  # 汉兵马俑博物馆
            '1485374',  # 狮子山楚王陵
            '1485363',  # 戏马台
            '1485385',  # 水下兵马俑
            '1469633',  # 汉化石像馆
            '1485361',  # 户部山
            '1793357'  # 云龙湖
        ]
    def get_commets(self,id,page):
        params={
            "action": "comment",
            "page": page,
            "order": 5,
            "poiid": id,
            "starLevel": "all",
        }
        res = self.session.get("https://place.qyer.com/poi.php?", params=params, headers=self.headers, timeout=10)
        return res.json()['data']

    def parse(self, datas):
        remarks = [{
            "publishTime": time.mktime(time.strptime(data["date"], "%Y-%m-%d")),
            "score": data['starlevel'],
            "content": self.p.sub("", data["content"].lower()),
            "Locate": '',
            "usefulCount": data['useful']
        } for data in datas]
        return remarks

    def main(self):
        for id in self.ploids:
            # 获取总页数
            commentCount = int(self.get_commets(id, 1)['total'])
            tatolNum = commentCount // 10 if commentCount % 10 == 0 else (commentCount // 10) + 1
            for i in range(tatolNum):
                datas = self.get_commets(id, i+1)['lists']
                remarks = self.parse(datas)
                for remark in remarks:
                    print(remark)
                remark_save('qiongyou',remarks)
            print(f'已完成id为{id}地区的评论爬取')

if __name__ == '__main__':
    qiong=QiongSpider()
    qiong.main()