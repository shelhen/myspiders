import requests
import time, re
from util import remark_save


class LvmaSpider(object):
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }
        self.ploids = {
            # 'productId','mainPlaceId'
            '182273': '101758',  # 汉文化景区
            '248449':'101146',  # 龟山汉墓
            # '248636':'100873',  # 云龙湖
        }
        self.p = re.compile(r'[^\w，。！？,.、:；℃]')
        self.session = requests.session()
    def get_comments(self, produId, polId):
        self.headers['referer'] = f"https://m.lvmama.com/ticket/piao-{produId}/comment?mainPlaceId={polId}"
        self.headers['signal'] = 'ab4494b2-f532-4f99-b57e-7ca121a137ca'
        url = 'https://m.lvmama.com/other/router/rest.do?'
        datas = []
        dataNum = 10
        i = 1
        while dataNum == 10:
            params = {
                'method': 'api.com.csa.cmt.getCmtCommentList',
                'version': '3.0.0',
                'productId': produId,
                'platForm': '',
                'recommend': 0,
                'newComment': 0,
                'picture': 0,
                'best': 0,
                'good': 0,
                'bad': 0,
                'relative': 0,
                'currentPage': i,
                'pageSize': 10,
                'isELong': 'N',
                'categoryName': 'PLACE',
                'mainPlaceId': polId,
                'firstChannel': 'TOUCH',
                'secondChannel': 'LVMM',
            }
            # 无需cookie，可直接拿到评论数据
            res = self.session.get(url, params=params, headers=self.headers, timeout=10)
            dataNum = len(res.json()['data']['list'])
            datas.extend(res.json()['data']['list'])
            i += 1
        return datas
    def parse(self, datas):
        remarks = [{
            "publishTime": time.mktime(time.strptime(data['createdTime'], "%Y-%m-%d %H:%M:%S")),
            "score": data['avgScore'],
            "content": self.p.sub("", data['content'].lower()),
            "Locate": '',
            "usefulCount": data['usefulCount']
        } for data in datas]
        return remarks
    def main(self):
        for proId, ploid in self.ploids.items():
            print(proId)
            datas = self.get_comments(proId, ploid)
            print(datas)

            remarks = self.parse(datas)
            for remark in remarks:
                print(remark)
            remark_save('lvmama', remarks)


if __name__ == '__main__':
    lvma = LvmaSpider()
    lvma.main()
